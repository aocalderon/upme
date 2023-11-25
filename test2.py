import rasterio
import argparse
import numpy as np
import pandas as pd
    
argParser = argparse.ArgumentParser("Sentinel 2 L2A converter from pixel to points.")
argParser.add_argument("-f", "--file", help="Raster file to read.")
args = argParser.parse_args()
infile = args.file

with rasterio.open(infile) as src:
    band1 = src.read(1)
    height = band1.shape[0]
    width = band1.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
    print(np.array(xs).flatten())
    vs = src.read(1)[rows,cols]
    lons = np.array(xs).flatten()
    lats = np.array(ys).flatten()
    vals = np.array(vs).flatten()
    d = {"lon": lons, "lat": lats, "value": vals}
    df = pd.DataFrame(d)
    print(df)
    df.to_csv("/tmp/raster.tsv", sep = "\t", index = False)