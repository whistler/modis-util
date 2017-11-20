from modis import _download

import os
import shutil
import unittest


class TestDownload(unittest.TestCase):
    TMP_DIR = '/tmp/modis'

    def test_scene_prefix(self):
        s3_prefix = _download._get_s3_prefix('MCD43A4.A2017006.h21v11.006.2017018074804')
        assert s3_prefix == 'MCD43A4.006/21/11/2017006/'

    def test_list_files(self):
        files = _download.list_files('MCD43A4.A2017006.h21v11.006.2017018074804')
        assert 'MCD43A4.006/21/11/2017006/BROWSE.MCD43A4.A2017006.h21v11.006.2017018025106.1.jpg' in files
        assert len(files) == 25

    def test_download_file(self):
        s3_key = 'MCD43A4.006/21/11/2017006/BROWSE.MCD43A4.A2017006.h21v11.006.2017018025106.1.jpg'
        _download.download_file(s3_key, self.TMP_DIR)
        assert os.path.exists(os.path.join(self.TMP_DIR, 'BROWSE.MCD43A4.A2017006.h21v11.006.2017018025106.1.jpg'))

    def test_filter_files_include(self):
        files = ['file_a.txt', 'file_b.txt', 'file_c.txt']
        filtered_files = _download._filter_files(files, ['_a', '_c.txt'], None)
        assert filtered_files == ['file_a.txt', 'file_c.txt']

    def test_filter_files_exclude(self):
        files = ['file_a.txt', 'file_b.txt', 'file_c.txt']
        filtered_files = _download._filter_files(files, None, ['_a', '_c.txt'])
        assert filtered_files == ['file_b.txt']

    def test_filter_files_noop(self):
        files = ['file_a.txt', 'file_b.txt', 'file_c.txt']
        filtered_files = _download._filter_files(files, None, None)
        assert filtered_files == files

    def test_download_scene(self):
        _download.download('MCD43A4.A2017006.h21v11.006.2017018074804', self.TMP_DIR, include=['_meta'])
        assert os.path.exists(os.path.join(self.TMP_DIR, 'MCD43A4.A2017006.h21v11.006.2017018074804_meta.json'))

    def tearDown(self):
        if os.path.exists(self.TMP_DIR):
            shutil.rmtree(self.TMP_DIR)