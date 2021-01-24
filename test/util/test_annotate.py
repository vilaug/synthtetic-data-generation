import sys
import unittest
from datetime import datetime

src_dir = "/workdir"
sys.path.insert(1, src_dir)

from src.util import annotate  # noqa: E402


class AnnotateTestCase(unittest.TestCase):

    def test_get_info(self):
        description = 'test'
        version = 0
        time_now = datetime.now()
        date_created = str(time_now.year) + "/" + str(time_now.month) + "/" + str(time_now.day)
        info = annotate.get_info(description, version, time_now)
        self.assertEqual(description, info['description'])
        self.assertEqual(version, info['version'])
        self.assertEqual(date_created, info['date_created'])

    def test_get_image_info(self):
        n_images = 1
        time_now = datetime.now()
        date_captured = str(time_now.year) + "/" + str(time_now.month) + "/" + str(time_now.day)
        resolution = (1200, 800)
        image_info = annotate.get_image_info(n_images, resolution, time_now)
        self.assertEquals(image_info[0]['id'], 0)
        self.assertEquals(image_info[0]['width'], resolution[0])
        self.assertEquals(image_info[0]['height'], resolution[1])
        self.assertEquals(image_info[0]['date_captured'], date_captured)

    def test_get_annotation_info_bad(self):
        x, y, width, height = 0, 0, 1, 1
        bounding_box = [x, y, width, height]
        bounding_boxes = [[('test', bounding_box)]]
        annotations = annotate.get_annotation_info(bounding_boxes, {}, {})
        self.assertEquals(len(annotations), 0)

    def test_get_annotation_info_good(self):
        x, y, width, height = 0, 0, 200, 200
        bounding_box = [x, y, width, height]
        bounding_boxes = [[('test_name', bounding_box)]]
        annotation = annotate.get_annotation_info(bounding_boxes, {}, {})[0]
        self.assertEqual(annotation['segmentation'], [x, y, x + width, y - height,
                                                      x + width, y, x, y - height])
        self.assertEqual(annotation['area'], width * height)
        self.assertEqual(annotation['bbox'], bounding_box)
        self.assertEqual(annotation['category_id'], -1)

    def test_get_category_id(self):
        name = 'test_name'
        category = 'test_cat'
        super_category = 'materials'
        category_id = 13
        ret_category_id = annotate.get_category_id(name, {super_category: {category: category_id}},
                                                   {name: category})
        self.assertEqual(category_id, ret_category_id)

    def test_get_category_info(self):
        name = 'test_cat'
        super_category = 'materials'
        category_id = 13
        category = annotate.get_category_info({super_category: {name: category_id}})[0]
        self.assertEqual(category['name'], name)
        self.assertEqual(category['supercategory'], super_category)
        self.assertEqual(category['id'], category_id)
