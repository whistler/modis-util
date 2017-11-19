from modis import coordinates

import unittest


class TestCoordinates(unittest.TestCase):

    def test_load_coordinates(self):
        coordinates_df = coordinates._load_coordinates()
        assert len(coordinates_df) == 648
        assert list(coordinates_df.columns) == ['iv', 'ih', 'lon_min', 'lon_max', 'lat_min', 'lat_max']

    def test_latlng_to_modis(self):
        v, h = coordinates.latlng_to_modis(1, 1)
        assert v == 8
        assert h == 18

    def test_invalid_lat(self):
        with self.assertRaises(ValueError):
            coordinates.latlng_to_modis(-90.1, 0)

    def test_invalid_lng(self):
        with self.assertRaises(ValueError):
            coordinates.latlng_to_modis(0, 180.1)

    def test_boundary_latlng(self):
        v, h = coordinates.latlng_to_modis(0, 0)
        assert 0 <= v <= 17
        assert 0 <= h <= 25

if __name__ == '__main__':
    unittest.main()