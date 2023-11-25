import argparse
import rasterio
from rasterio  import transform

argParser = argparse.ArgumentParser("Sentinel 2 L2A converter from pixel to points.")
argParser.add_argument("-f", "--file", help="Raster file to read.")
args = argParser.parse_args()
filename = args.file

raster = rasterio.open(filename)
sid = filename.split(".")[0]
band = sid.split("_")[-1]

#rows = raster.width
#cols = raster.height
rows = 10
cols = 2

print(f"{args.file}\t{rows}\t{cols}")

with open(f"P{sid}.tsv", 'w') as outfile:
    for col in range(cols):
        for row in range(rows):
            value = raster.read(1)[row,col]
            x, y = transform.xy(raster.transform, row, col)
            if value != 0.0:
                outfile.write(f"{x}\t{y}\t{band}\t{value}\n")
        print(f"{col} done.")

