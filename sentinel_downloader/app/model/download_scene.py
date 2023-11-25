from odc.stac import stac_load
import planetary_computer as pc
import os
import threading

from model import imagery_to_float
from model import clock_time_now


def download(args):
    """
    Download a scene given its ID.

    Args:
        args (tuple): A tuple containing the scene ID, the catalog, the start index, the spatial resolution, the output folder, and the configuration.

    Returns:
        None

    Raises:
        None
    """

    sid, catalog, start, resolution, output_folder, cfg = args
    year_month = sid.split("_")[2][:6]
    year = year_month[:4]
    month = year_month[4:]

    query = catalog.search(
        collections = ["sentinel-2-l2a"],
        datetime = f"{year}-{month}",
        query = {"id": dict(eq=sid)}
    )

    items = list(query.items())
    thread_id = threading.get_ident()

    if len(items) != 0:
        print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\tSCENE\tFOUND")

        try:
            imagery = stac_load(
                items,
                bands = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B11", "B12"],
                chunks = {"x": 2048, "y": 2048},
                stac_cfg = cfg,
                patch_url = pc.sign,
                resolution = resolution,
            )

            bands = list(imagery.data_vars)

            print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\tSCENE\tDOWNLOAD")
            for band in bands:
                print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\t{band}\tSTART")

                output_path = os.path.join(output_folder, f"{sid}_{band}.tif")
                imagery_to_float.convert(imagery.get(band)).compute().odc.write_cog(output_path, overwrite = True)

                print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\t{band}\tEND")

            print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\tSCENE\tDONE")

        except Exception as e:
            print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\tSCENE\tERROR")

    else:
        print(f"THREAD ID:{thread_id}\tINFO\t{clock_time_now.get_time()}\t{sid}\tSCENE\tNOT FOUND")