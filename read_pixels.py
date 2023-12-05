import rasterio
import argparse
import numpy as np
import pandas as pd
    
argParser = argparse.ArgumentParser("Sentinel 2 L2A converter from pixel to points.")
argParser.add_argument("-i", "--input", help="Raster file to read.")
argParser.add_argument("-o", "--output", help="File to save.")
argParser.add_argument("-c", "--coordinates", help="Keep the coordinates.", action=argparse.BooleanOptionalAction)
args = argParser.parse_args()
infile  = args.input
outfile = args.output
coords  = args.coordinates

with rasterio.open(infile) as raster:
    band1  = raster.read(1)
    height = band1.shape[0]
    width  = band1.shape[1]
    
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    vs = band1[rows,cols]
    vals = np.array(vs).flatten()

    if coords:
        xs, ys = rasterio.transform.xy(raster.transform, rows, cols)
        lons = np.array(xs).flatten()
        lats = np.array(ys).flatten()
        d = {"lon": lons.astype(int), "lat": lats.astype(int), "value": vals.astype(int)}
    else:
        d = {"value": vals.astype(int)}

    df = pd.DataFrame(d)
    df = df[(df['value'] > 0.0)]
    print(f"Saving {outfile}...")
    df.to_csv(outfile, sep = "\t", index = False)