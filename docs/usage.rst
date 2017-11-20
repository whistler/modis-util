Usage
=====

Search
++++++

Search for a scene::

    import modis
    import datetime
    scenes = modis.search(modis.products.MCD43A4_006, 49.2827, 123.1207, datetime.date(2017, 11, 15))

Download
++++++++

Download complete dataset for a scene::

    modis.download('MCD43A4.A2016001.h25v04.006.2016174082825_B05', 'modis_data')

Download only certain files of a scene, you can use any part of the filename in the `include` list::

    modis.download('MCD43A4.A2016001.h25v04.006.2016174082825_B05', include=['BROWSE'])
