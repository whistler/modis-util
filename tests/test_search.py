from modis import search
from modis.products import ModisProducts

from datetime import date
import unittest


class TestSearch(unittest.TestCase):

    def test_search(self):
        vancouver_lat = 49.2827
        vancouver_lng = 123.1207
        search_date = date(2016, 1, 1)
        results = search.search(ModisProducts.MCD43A4_006, vancouver_lat, vancouver_lng, search_date)
        assert results == ['MCD43A4.A2016001.h25v04.006.2016174082825']

    def test_get_s3_key(self):
        search_date = date(2016, 1, 1)
        assert search._get_s3_key('MOD09GA.006', search_date) == 'MOD09GA.006/2016-01-01_scenes.txt'

    def test_get_s3_file(self):
        filename = 'MCD43A4.006/2017-10-23_scenes.txt'
        data = search._get_s3_file(filename)
        lines = data.split('\n')
        assert lines[0] == "date,download_url,gid"