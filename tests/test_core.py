from modis import core

import unittest


class TestCore(unittest.TestCase):

    def test_parse_scene_id(self):
        product_id, v, h = core.parse_scene_id('MCD43A4.A2016001.h18v17.006.2016174081859')
        assert product_id == 'MCD43A4'
        assert v == 17
        assert h == 18