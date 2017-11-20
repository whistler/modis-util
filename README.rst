Modis-Util
========================

Modis-Util is a tool that makes it easy to search and download `MODIS <https://modis.gsfc.nasa.gov/>`_ data on `AWS
<https://aws.amazon.com/public-datasets/modis/>`_.

Install
+++++++

Install this package using pip::

    pip install modis-util


Usage
+++++

Search for a scene::

    import modis
    import datetime

    product = modis.products.MCD43A4_006
    latitude = 49.2827
    longitude = 123.1207
    date = datetime.date(2017, 1, 1)

    scenes = modis.search(product, latitude, longitude, date)
    # scenes = ['MCD43A4.A2017001.h25v04.006.2017014061357']

Download complete dataset for a scene::

    scene_id = 'MCD43A4.A2016001.h25v04.006.2016174082825_B05'
    destination_path = 'modis_data'
    modis.download(scene_id, destination_path)

Download only certain files of a scene, you can use any part of the filename in the `include` list::

    modis.download(scene_id, destination_path, include=['BROWSE'])
---------------


