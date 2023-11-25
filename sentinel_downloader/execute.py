"""
Sentinel 2 L2A downloader from Planetary Computer.

Version developed by David Jimenez Mora, d.jimenezm2@uniandes.edu.co.
11/2023
"""

import argparse
import config as cf
import os
import psutil

from app.controller import main

def parse_arguments():
    """
    Parse command line arguments.

    Args:
        None

    Returns:
        argparse.Namespace: The parsed arguments.

    Raises:
        None
    """

    arg_parser = argparse.ArgumentParser("Sentinel 2 L2A downloader from Planetary Computer.")
    arg_parser.add_argument("-f", "--file", default = f"ids.tsv", help = "File with ids for the scenes to be downloaded (Default: ids.tsv).")
    arg_parser.add_argument("-p", "--num_processes", default = os.cpu_count(), help = "Number of processors (Default: all available).")
    arg_parser.add_argument("-m", "--max_memory", default = psutil.virtual_memory().total, help = "Maximum memory to use in bytes (Default: all available).")
    arg_parser.add_argument("-r", "--resolution", default = 10, help = "Spatial resolution for resampling in meters (Default: 10).")
    arg_parser.add_argument("-s", "--start", default = 0, help = "Start at this index. (Default: 0)")

    return arg_parser.parse_args()

def print_info(args, cf):
    """
    Print information about the program.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    mem_size = int(args.max_memory)
    mem_size, mem_unit = (mem_size, "B") if mem_size < 1024 else (mem_size / 1024, "KB") if mem_size < 1024**2 else (mem_size / (1024**2), "MB") if mem_size < 1024**3 else (mem_size / (1024**3), "GB")
    mem_size = round(mem_size, 2)

    print("\nSentinel 2 L2A downloader from Planetary Computer.")
    print("Version developed by David Jimenez Mora")
    print("d.jimenezm2@uniandes.edu.co")

    print(f"\nDownloading scenes from {args.file} starting at index {args.start} and resolution of {args.resolution}.")
    print(f"Executing with {args.num_processes} processes and {mem_size}{mem_unit} of memory.")
    print(f"All downloaded scenes will be saved in {cf.data_dir}bands folder.\n")
    print("#" * 100)

#If the file is run directly, execute the view.
if __name__ == '__main__':
    args = parse_arguments()

    if args.num_processes > os.cpu_count():
        print("ERROR: Number of processes exceeds available CPUs.")
        exit()

    elif int(args.max_memory) > psutil.virtual_memory().total:
        print("ERROR: Memory limit exceeds available memory.")
        exit()

    elif args.start < 0:
        print("ERROR: Start index must be greater than or equal to zero.")
        exit()

    else:
        print_info(args, cf)
        main.begin(args, cf)
