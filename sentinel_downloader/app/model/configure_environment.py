import os

def configure(cf):
    """
    Configure the processing environment.
    The download script will create a folder called "bands" in the same directory as the script.

    Args:
        None

    Returns:
        tuple: A tuple containing the configuration, the parent directory, and the output folder.

    Raises:
        None
    """

    cfg = {
        "sentinel-2-l2a": {
            "assets": {
                "*": {"data_type": "uint16", "nodata": 0},
                "SLC": {"data_type": "uint8", "nodata": 0},
            },
        },
        "*": {"warnings": "ignore"},
    }

    # Define the output folder for storing downloaded bands
    output_folder = os.path.join(cf.data_dir, "bands")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return cfg, cf.file_dir, output_folder
