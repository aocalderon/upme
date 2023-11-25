import os
import csv

def check(sids: list, cf):
    """
    Checks if the scenes have been downloaded.

    Args:
        sids (list): A list of scene IDs.
        cf (config): The configuration file.

    Returns:
        bool: True if all scenes have been downloaded, False otherwise.

    Raises:
        None
    """

    bands = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B11", "B12"]

    downloaded_images = os.listdir(f"{cf.data_dir}bands")
    missing_ids = []

    for sid in sids:
        for band in bands:
            image_name = f"{sid}_{band}.tif"

            if image_name not in downloaded_images:
                missing_ids.append(sid)

    if len(missing_ids) == 0:
        return True

    else:
        missing_ids_file_path = f"{cf.data_dir}missing_ids.tsv"

        with open(missing_ids_file_path, "w", newline = "", encoding = "utf-8") as tsv_file:
            writer = csv.writer(tsv_file)

            for missing_id in missing_ids:
                writer.writerow([missing_id])

        return False