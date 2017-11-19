import re

# S3 Bucket with Modis data
MODIS_BUCKET = 'modis-pds'


def parse_scene_id(scene_id):
    """
    Parses a scene id
    Args:
        scene_id (string): ID of modis scene e.g. MCD43A4.A2016001.h17v16.006.2016174081739

    Returns:
        product_id (string): Type of Modis product (excluding version)
        h (int): Horizontal coordinate of Modis grid
        v (int): Vertical coordinate of Modis grid
    """
    matches = re.search('^(\w{7})\.\w*\.h(\d*)v(\d*)', scene_id)
    product_id = matches.group(1)
    v = int(matches.group(3))
    h = int(matches.group(2))
    return product_id, v, h