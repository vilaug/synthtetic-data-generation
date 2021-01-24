import sys
import unittest
from pathlib import Path

import bpy

src_dir = "/workdir"
sys.path.insert(1, src_dir)
from src.blender.object import Object  # noqa: E402
from src.blender.crush import Crush  # noqa: E402
from test.blender.test_blender import BlenderTestCase  # noqa: E402


class CrushTestCase(unittest.TestCase):
    # Runs before every test
    def setUp(self):
        self.crush = Crush()
        self.temporary_path = './tmp/'
        self.blender = self.crush.blender
        self.blender.clear_scene([])
        self.background = '/Backgrounds/Blue_Plastic_roller.jpg'

    # Runs after every test
    def tearDown(self):
        self.crush.blender.clear_scene([])

    def test_export_model(self):
        BlenderTestCase.import_testing_object(self)
        self.crush.export_model(bpy.data.objects[1], self.temporary_path)
        self.assertEqual(True, Path('./tmp/' + bpy.data.objects[1].name + '.obj').is_file())

    def test_crush_model(self):
        BlenderTestCase.import_testing_object(self)
        obj = Object(src_dir + '/test/test_objects/test_cube.obj',
                     'random', 'random', 'random', 420)
        self.crush.crush_model(obj, self.temporary_path)
        self.assertEqual(True,
                         Path(self.temporary_path + bpy.data.objects[1].name + '.obj').is_file())


if __name__ == '__main__':
    unittest.main(argv=sys.argv[0:1])
