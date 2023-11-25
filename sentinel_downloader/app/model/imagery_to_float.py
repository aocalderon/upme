import odc.stac

def convert(imagery: odc.stac.stac_load):
    """
    Convert imagery to float32.

    Args:
        imagery (odc.stac.stac_load): Imagery to convert to float32.

    Returns:
        odc.stac.stac_load: Imagery converted to float32.

    Raises:
        Exception: An error occurred converting the imagery.
    """

    try:
        _imagery = imagery.astype("float32")
        nodata = imagery.attrs.get("nodata", None)

        if nodata is None:
            return _imagery

        return _imagery.where(_imagery != nodata)

    except Exception as e:
        raise e