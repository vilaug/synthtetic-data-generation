import sys
import unittest

import bpy

src_dir = "/workdir"
sys.path.insert(1, src_dir)
from src.blender.scene import Scene  # noqa: E402


class SceneTestCase(unittest.TestCase):
    camera_location = [0, 0, 2]
    camera_rotation = [0, 0, 0]
    light_location = [0, 0, 2]
    light_energy = 1
    light_type = 'POINT'

    # Runs before every test
    def setUp(self):
        self.camera_location = [0, 0, 2]
        self.camera_rotation = [0, 0, 0]
        self.light_location = [0, 0, 2]
        self.light_energy = 1
        self.light_type = 'POINT'
        self.scene = Scene(self.camera_location, self.camera_rotation, self.light_location,
                           self.light_energy, self.light_type)

    # Runs after every test
    def tearDown(self):
        self.scene.clear_scene([])

    def test_setup_camera(self):
        cam = bpy.context.scene.camera
        self.assertEqual(self.camera_location,
                         [cam.location.x, cam.location.y, cam.location.z])
        self.assertEqual(self.camera_rotation,
                         [cam.rotation_euler[0], cam.rotation_euler[0], cam.rotation_euler[0]])

    def test_setup_light(self):
        light_data = bpy.data.lights['Light']
        light_object = bpy.data.objects['Light']
        self.assertEqual(self.light_energy, light_data.energy)
        self.assertEqual(self.light_type, light_data.type)
        self.assertEqual(self.light_location,
                         [light_object.location.x, light_object.location.y, light_object.location.z]
                         )


if __name__ == '__main__':
    unittest.main(argv=sys.argv[0:1])
