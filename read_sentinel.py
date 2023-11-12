import dask.distributed
import dask.utils
import planetary_computer as pc
from pystac_client import Client
import os
from odc.stac import configure_rio, stac_load
import csv
import argparse
from datetime import datetime

argParser = argparse.ArgumentParser("Sentinel 2 L2A downloader from Planetary Computer.")
argParser.add_argument("-f", "--file",  default="ids.tsv", help="File with ids for the scenes to be downloaded.")
argParser.add_argument("-w", "--workers", default=-1, help="Number of workers.")
argParser.add_argument("-r", "--resolution", default=10, help="Spatial resolution for resampling (in meters).")
argParser.add_argument("-s", "--start", default=0, help="Start at this index.")
args = argParser.parse_args()

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

def clocktime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def to_float(imagery):
    _imagery = imagery.astype("float32")
    nodata = imagery.attrs.get("nodata", None)
    if nodata is None:
        return _imagery
    return _imagery.where(_imagery != nodata)

if __name__ == "__main__":
    with dask.distributed.LocalCluster(n_workers=int(args.workers), dashboard_address=':8100') as cluster:
        with dask.distributed.Client(cluster) as client:
            print(cluster)
            print(client)
            configure_rio(cloud_defaults=True, client=client)
    
            catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier = pc.sign_inplace)
            sids = []

            # Define the path to the TSV file containing scene IDs...
            input_file = args.file
            sids_path = os.path.join(script_directory, input_file)
            with open(input_file, 'r', newline='') as tsvfile:
                tsvreader = csv.reader(tsvfile, delimiter='\t')
                # Add scene IDs to the list...
                for row in tsvreader:
                    sids.append(row[0])

            start = int(args.start)
    
            print(f"INFO\t{clocktime()}\tBULK\tDOWNLOAD\tSTART")
            for sid in sids[start:]:
                # Extract the year and month from the scene ID...
                year_month = sid.split("_")[2][:6]
                year = year_month[:4]
                month = year_month[4:]
                query =  catalog.search(
                    collections=["sentinel-2-l2a"], 
                    datetime=f"{year}-{month}", 
                    query ={"id":dict(eq=sid)}
                    )
                items = list(query.items())
                
                # Check if the scene was found...
                if len(items) != 0:
                    print(f"INFO\t{clocktime()}\t{sid}\tSCENE\tFOUND")
                
                    resolution = int(args.resolution)
                
                    try:
                        imagery = stac_load(
                            items, 
                            #bands=["B02","B03","B04","B05","B06","B07","B08","B11","B12","SCL"],
                            bands=["SCL"],
                            chunks={"x": 2048, "y": 2048}, 
                            stac_cfg=cfg,
                            patch_url = pc.sign,
                            resolution=resolution,
                        )
                        bands = list(imagery.data_vars)
                
                        print(f"INFO\t{clocktime()}\t{sid}\tSCENE\tDOWNLOAD")
                        for band in bands:
                            print(f"INFO\t{clocktime()}\t{sid}\t{band}\tSTART")
                            output_path = os.path.join(output_folder, f"{sid}_{band}.tif")
                            to_float(imagery.get(band)).compute().odc.write_cog(output_path, overwrite=True)
                            print(f"INFO\t{clocktime()}\t{sid}\t{band}\tEND")
                        print(f"INFO\t{clocktime()}\t{sid}\tSCENE\tDONE")
                        
                    except Exception as e:
                        print(f"INFO\t{clocktime()}\t{sid}\tSCENE\tERROR")
                else:
                    print(f"INFO\t{clocktime()}\t{sid}\tSCENE\tNOT FOUND")
                    
            print(f"{clocktime()}\tBULK\tDOWNLOAD\tEND")

