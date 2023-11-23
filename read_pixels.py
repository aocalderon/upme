import argparse
import rasterio

argParser = argparse.ArgumentParser("Sentinel 2 L2A converter from pixel to points.")
argParser.add_argument("-f", "--file", help="Raster file to read.")
args = argParser.parse_args()

raster = rasterio.open(args.file)

rows = 100
cols = 100
for col in range(cols):
    for row in range(rows):
        value = raster.read(1)[row,col]
        if value != 0.0:
            print(f"{row}\t{col}\t{value}", end="")
        else:
            print(".", end="")
    print("\n")
