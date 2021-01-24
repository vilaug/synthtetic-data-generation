import unittest
import sys

src_dir = "/workdir"
sys.path.insert(1, src_dir)

from src.server import main  # noqa: E402


class ServerMainTestCase(unittest.TestCase):

    def test_index(self):
        status_code = main.app.test_client().get("/").status_code
        self.assertEqual(200, status_code)

    def test_download(self):
        status_code = main.app.test_client().get('/download_images').status_code
        self.assertEqual(200, status_code)

    def test_generate_get(self):
        status_code = main.app.test_client().get('/generate').status_code
        self.assertEqual(200, status_code)

    def test_generate_post_bad_request(self):
        status_code = main.app.test_client().post('/generate',
                                                  data=dict(HDPE=50,
                                                            image_count=5,
                                                            object_count=1)).status_code
        self.assertEqual(400, status_code)
