import argparse

argParser = argparse.ArgumentParser("Sentinel 2 L2A downloader from Planetary Computer.")
argParser.add_argument("-m", "--missing", help="File for missing ids.")
argParser.add_argument("-f", "--found",   help="File for found ids.")
argParser.add_argument("-o", "--output",   help="File save still missing ids and bands.")
args = argParser.parse_args()

with open(args.missing, 'r') as m:
    missing = m.read().splitlines()
with open(args.found, 'r') as f:
    found = f.read().splitlines()

ids_bands = list(set(missing) - set(found))

with open(args.output, 'w') as output:
    for id_band in ids_bands:
        band = id_band.split("_")[-1]
        id = "_".join(id_band.split("_")[:-1])
        output.write(f"{id}\t{band}\n")
