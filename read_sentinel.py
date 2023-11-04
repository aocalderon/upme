import dask.distributed 
import dask.utils
import planetary_computer as pc
from pystac_client import Client
import os
from odc.stac import configure_rio, stac_load
import csv


cfg = {
    "sentinel-2-l2a":{
        "assets":{
            "*":{"data_type":"uint16", "nodata":0},
            "SLC":{"data_type":"uint8", "nodata":0},
        },
    },
    "*":{"warnings":"ignore"},
}

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the output folder for storing downloaded bands
output_folder = os.path.join(script_directory, "bands")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def to_float(imagery):
    _imagery = imagery.astype("float32")
    nodata = imagery.attrs.get("nodata", None)
    if nodata is None:
        return _imagery
    return _imagery.where(_imagery != nodata)

        
if __name__ == "__main__":
    client = dask.distributed.Client()
    configure_rio(cloud_defaults=True, client=client)
    
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier = pc.sign_inplace)
    sids = []
    
    # Define the path to the TSV file containing scene IDs
    sids_path = os.path.join(script_directory, "ids.tsv")
    with open('ids.tsv', 'r', newline='') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        
        # Add scene IDs to the list
        for row in tsvreader:
            sids.append(row[0])
            
            
    for sid in sids:
        # Extract the year and month from the scene ID
        year_month = sid.split("_")[2][:6]
        year = year_month[:4]
        month = year_month[4:]
        query =  catalog.search(
            collections=["sentinel-2-l2a"], 
            datetime=f"{year}-{month}", 
            query ={"id":dict(eq=sid)}
            )
        items = list(query.items())
        
        # Check if the scene was found
        if len(items) != 0:
            print(f"Found: {sid} scene")
        
        resolution = 10
        
        try:
            imagery = stac_load(
            items, 
            bands=["B02","B03","B04","B05","B06","B07","B08","B11","B12","SCL"],
            chunks={"x":2048, "y":2048}, 
            stac_cfg=cfg,
            path_url = pc.sign,
            resolution=resolution,
            )
            bands = list(imagery.data_vars)
            print(f"Bands: {','.join(bands)}")
        
            for band in bands:
                print(f"Downloading {band}...")
                output_path = os.path.join(output_folder, f"{sid}_{band}.tif")
                to_float(imagery.get(band)).compute().odc.write_cog(output_path, overwrite=True)
            print(f"Done {sid}.")
            
        except Exception as e:
            print(f"Error: {sid} scene")