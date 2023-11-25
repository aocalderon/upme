"""import sys

# Imprimir el directorio actual de trabajo
print("Directorio actual de trabajo:", sys.path[0])

# Imprimir los directorios en los que Python está buscando módulos
print("Directorios de búsqueda de módulos:")
for path in sys.path:
    print(path)
"""

import dask.distributed
import dask.utils
import planetary_computer as pc
from pystac_client import Client
import os
from odc.stac import configure_rio
import csv
import argparse
from multiprocessing import Pool

from model import configure_environment
from model import clock_time_now
from model import download_scene
from model import check_downloads

def begin(args: argparse.Namespace, cf):
    """
    Execute the main program.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    cfg, script_directory, output_folder = configure_environment.configure(cf)

    with dask.distributed.LocalCluster(n_workers = 1,threads_per_worker = int(args.num_processes), dashboard_address = ':8100', memory_limit = int(args.max_memory)) as cluster:
        with dask.distributed.Client(cluster) as client:
            print("\nCluster and client info:")
            print(cluster)
            print(client, "\n")

            configure_rio(cloud_defaults = True, client = client)

            catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier = pc.sign_inplace)
            sids = []

            # Define the path to the TSV file containing scene IDs...
            input_file = f"{cf.data_dir}{args.file}"
            sids_path = os.path.join(script_directory, input_file)

            with open(input_file, 'r', newline = '') as tsv_file:
                tsv_reader = csv.reader(tsv_file, delimiter = '\t')

                # Add scene IDs to the list...
                for row in tsv_reader:
                    if len(row) > 0:
                        sids.append(row[0])

            start = int(args.start)
            sids = sids[start:]

            print(f"INFO\t{clock_time_now.get_time()}\tBULK\tDOWNLOAD\tSTART")

            # Use multiprocessing pool to parallelize scene downloads
            num_processes = int(args.num_processes)

            with Pool(processes = num_processes) as pool:
                pool.map(download_scene.download, [(sid, catalog, start, int(args.resolution), output_folder, cfg) for sid in sids])

            print(f"{clock_time_now.get_time()}\tBULK\tDOWNLOAD\tEND")

    all_downloaded = check_downloads.check(sids, cf)

    if all_downloaded == True:
        print("\nAll scenes downloaded successfully.")

    else:
        print("\nSome scenes were not downloaded successfully. Downloading missing scenes...\n")
        args.file = f"{cf.data_dir}missing_ids.tsv"

        begin(args, cf)