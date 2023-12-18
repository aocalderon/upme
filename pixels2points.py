import rasterio
import numpy as np
import pandas as pd

def main(infile, outpath, coords, n):
    """Process infile block-by-block and write to a new file"""

    filename = args.input.split(".")[0].split("/")[-1]
    arr = filename.split("_")
    band = arr[-1]
    sid = "_".join(arr[:-1])
    print(f"{sid}\t{band}")
    print(f"n={n}")
    with rasterio.Env():
        with rasterio.open(infile) as src:
            # Update the profile to use blocks and allowing tiling...
            profile = src.profile
            profile.update(blockxsize=n, blockysize=n, tiled=True)
            print(profile)

            with rasterio.open("/tmp/t", "w", **profile) as dst:
                # Collect the windows based on the blocks...
                windows = [window for ij, window in dst.block_windows()]

                # This generator comprehension gives us raster data arrays for each window...
                data_gen = ( src.read(window=window) for window in windows )

                # Let's iterate over the windows and generator...
                for window, data in zip( windows, data_gen ):
                    vals = data.flatten() # Extract pixel values...

                    # Create grids for each block...
                    X = np.arange(window.width)  + window.col_off
                    Y = np.arange(window.height) + window.row_off
                    cols, rows = np.meshgrid(X, Y)

                    # Get data columns from the image with coordinates if required...
                    if band == "B02":
                        xs, ys = rasterio.transform.xy(src.transform, rows, cols) 
                        lons = np.array(xs).flatten()
                        lats = np.array(ys).flatten()
                        d = {"lon": lons.astype(int), "lat": lats.astype(int), band: vals.astype(int)}
                    else:
                        d = {band: vals.astype(int)}

                    # Create the dataframe and filter out null values...
                    df = pd.DataFrame(d)

                    # Save data just for valid blocks...
                    if df.size > 0:
                        outfile = f"{outpath}/{sid}_BLOCK_{window.col_off}_{window.row_off}_{band}.tsv"
                        print(f"{outfile}")
                        df.to_csv(outfile, sep = "\t", index = False)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Raster translator.")
    parser.add_argument("input", metavar="INPUT", help="Input file name.")
    parser.add_argument("outpath", metavar="OUTPUT", help="Output path route.")
    parser.add_argument("--coords", action=argparse.BooleanOptionalAction, help="Print coordinates.")
    parser.add_argument("--n", type = int, default=2048, help="Side size of the block.")
    args = parser.parse_args()

    main(args.input, args.outpath, args.coords, args.n)
