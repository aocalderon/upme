"""thread_pool_executor.py

Operate on a raster dataset window-by-window using a ThreadPoolExecutor.

Simulates a CPU-bound thread situation where multiple threads can improve
performance.

With -j 4, the program returns in about 1/4 the time as with -j 1.
"""

import concurrent.futures
import multiprocessing
import numpy as np
import pandas as pd

import rasterio

def mycompute(input):
    f = input.flatten()
    return f


def main(infile, outfile, num_workers = 4):
    """Process infile block-by-block and write to a new file

    The output is the same as the input, but with band order
    reversed.
    """

    chunk_size = 512
    coords = True
    with rasterio.Env():
        with rasterio.open(infile) as src:
            # Create a destination dataset based on source params. The
            # destination will be tiled, and we'll process the tiles
            # concurrently.
            profile = src.profile
            profile.update(blockxsize = chunk_size, blockysize = chunk_size, tiled = True)

            # Materialize a list of destination block windows
            # that we will use in several statements below.
            windows = [window for ij, window in src.block_windows()]

            # This generator comprehension gives us raster data
            # arrays for each window. Later we will zip a mapping
            # of it with the windows list to get (window, result)
            # pairs.
            data_gen = (src.read(window=window) for window in windows)

            for window, data in zip( windows, data_gen ):
                vals = data.flatten()
                cols, rows = np.meshgrid(np.arange(window.width) + window.col_off, np.arange(window.height) + window.row_off)
                if coords:
                    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
                    lons = np.array(xs).flatten()
                    lats = np.array(ys).flatten()
                    d = {"lon": lons.astype(int), "lat": lats.astype(int), "value": vals.astype(int)}
                else:
                    d = {"value": vals.astype(int)}

                df = pd.DataFrame(d)
                df = df[(df['value'] > 0.0)]
                if df.size > 0:
                    outfile = f"tsvs/Q_{window.col_off}_{window.row_off}.tsv"
                    print(f"Saving {outfile}...")
                    df.to_csv(outfile, sep = "\t", index = False)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers = num_workers) as executor:
                # We map the compute() function over the raster
                # data generator, zip the resulting iterator with
                # the windows list, and as pairs come back we
                # write data to the destination dataset.

                for window, vals in zip( windows, executor.map(mycompute, data_gen) ):
                    cols, rows = np.meshgrid(np.arange(window.width) + window.col_off, np.arange(window.height) + window.row_off)
                    if coords:
                        xs, ys = rasterio.transform.xy(src.transform, rows, cols)
                        lons = np.array(xs).flatten()
                        lats = np.array(ys).flatten()
                        d = {"lon": lons.astype(int), "lat": lats.astype(int), "value": vals.astype(int)}
                    else:
                        d = {"value": vals.astype(int)}

                    df = pd.DataFrame(d)
                    df = df[(df['value'] > 0.0)]
                    if df.size > 0:
                        outfile = f"tsvs/T_{window.col_off}_{window.row_off}.tsv"
                        print(f"Saving {outfile}...")
                        df.to_csv(outfile, sep = "\t", index = False)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Concurrent raster processing demo")
    parser.add_argument("input", metavar="INPUT", help="Input file name")
    parser.add_argument("output", metavar="OUTPUT", help="Output file name")
    parser.add_argument(
        "-j",
        metavar="NUM_JOBS",
        type=int,
        default=multiprocessing.cpu_count(),
        help="Number of concurrent jobs",
    )
    args = parser.parse_args()

    main(args.input, args.output, args.j)
