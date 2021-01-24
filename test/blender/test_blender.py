import sys
import argparse
import unittest
from pathlib import Path

import bpy

src_dir = "/workdir"
sys.path.insert(1, src_dir)
from src.blender.blender import Blender  # noqa: E402
from src.blender.object import Object  # noqa: E402
import src.util.parser as p  # noqa: E402


class BlenderTestCase(unittest.TestCase):
    # Runs before every test
    def setUp(self):
        self.blender = Blender()
        self.blender.clear_scene([])
        self.background = 'BYWA0419.jpg'

    # Runs after every test
    def tearDown(self):
        self.blender.clear_scene([])

    def test_background_name(self):
        self.blender.setup_background_plane(self.background, 2, 2, None)
        self.assertEqual("background", bpy.context.active_object.name)

    def test_background_dimensions_x(self):
        self.blender.setup_background_plane(self.background, 2, 2, None)
        # IMPORTANT: need to be ran to let the API update the scene
        bpy.context.view_layer.update()
        self.assertEqual(2, bpy.context.active_object.dimensions.x)

    def test_background_dimensions_y(self):
        self.blender.setup_background_plane(self.background, 2, 3, None)
        # IMPORTANT: need to be ran to let the API update the scene
        bpy.context.view_layer.update()
        self.assertEqual(3, bpy.context.active_object.dimensions.y)

    def test_background_location(self):
        self.blender.setup_background_plane(self.background, 2, 3, None)
        # IMPORTANT: need to be ran to let the API update the scene
        bpy.context.view_layer.update()
        plane_location = bpy.context.active_object.location
        self.assertEqual((0.0, 0.0, 0.0), (plane_location.x, plane_location.y, plane_location.z))

    def test_import_object(self):
        object_pack = self.import_testing_object()
        self.assertEqual(object_pack[0].name, bpy.data.objects[1].name[:9])

    def test_set_orientation(self):
        object_pack = self.import_testing_object()
        self.blender.set_object_orientation(object_pack[0], [1, 1, 1])
        self.assertAlmostEqual(1, object_pack[0].rotation_euler[0], 4)
        self.assertAlmostEqual(1, object_pack[0].rotation_euler[1], 4)
        self.assertAlmostEqual(1, object_pack[0].rotation_euler[2], 4)

    def test_set_location(self):
        object_pack = self.import_testing_object()
        self.blender.set_object_location(object_pack[0], [1, 1, 1])
        self.assertAlmostEqual(1, object_pack[0].location.x, 4)
        self.assertAlmostEqual(1, object_pack[0].location.y, 4)

    def import_testing_object(self):
        object_name = 'test_cube'
        object_path = src_dir + "/test/test_objects/" + object_name + ".obj"
        obj = Object(object_path, 'random', 'random', 'random', 420)
        obj.randomize_object(420)
        self.blender.setup_object(obj)
        return [bpy.data.objects[1], obj, object_name]

    def test_set_render_device(self):
        self.blender.set_render_device('CPU')
        self.assertEqual('CPU', bpy.context.scene.cycles.device)
        self.blender.set_render_device('GPU')
        self.assertEqual('GPU', bpy.context.scene.cycles.device)

    def test_set_render_output_parameters(self):
        self.blender.set_render_output_parameters()
        scene = bpy.context.scene
        configuration = p.Parser().parse_long_term_configuration(Path(
            '/workdir' + r"/configuration.yaml"))
        self.assertEqual(configuration['render']['res_width'], scene.render.resolution_x)
        self.assertEqual(configuration['render']['res_height'], scene.render.resolution_y)
        self.assertEqual(configuration['render']['res_percentage'],
                         scene.render.resolution_percentage)

    def test_color_object(self):
        object_pack = self.import_testing_object()
        color = (0.5, 0.6, 0.7, 0)
        self.blender.color_object(object_pack[0], color)
        color_of_object = object_pack[0].active_material.diffuse_color
        self.assertAlmostEqual(0.5, color_of_object[0])
        self.assertAlmostEqual(0.6, color_of_object[1])
        self.assertAlmostEqual(0.7, color_of_object[2])
        self.assertAlmostEqual(0, color_of_object[3])

    def test_set_softbody(self):
        self.import_testing_object()
        self.blender.activate_model(bpy.data.objects[1])
        self.blender.set_softbody()
        # Check all necessary values
        settings_softbody = bpy.context.object.modifiers["Softbody"].settings
        self.assertEqual(False, settings_softbody.use_goal)
        self.assertEqual(100, settings_softbody.plastic)
        self.assertEqual(10.0, settings_softbody.bend)

    def test_setup_cage(self):
        self.import_testing_object()
        self.blender.activate_model(bpy.data.objects[1])
        self.blender.setup_cage(bpy.data.objects[1])
        # cube = 2m each side
        # sqrt(2^2+2^2)*1,05 (from the offset of 0.1/2)
        # = 2.97
        self.assertAlmostEqual(round(bpy.data.objects[3].dimensions.x), 3)

    def test_set_mesh_deform(self):
        self.import_testing_object()
        # add cage to bind
        self.blender.setup_cage(bpy.data.objects[1])
        self.blender.activate_model(bpy.data.objects[1])
        sphere = self.blender.get_model("Sphere")
        self.blender.set_mesh_deform(sphere)
        self.assertEqual(bpy.context.object.modifiers["MeshDeform"].object, sphere)
        self.assertEqual(bpy.context.object.modifiers["MeshDeform"].precision, 3)

    def test_get_model(self):
        self.import_testing_object()
        obj = bpy.data.objects[1]
        self.assertEqual(obj, self.blender.get_model(obj.name))

    def test_setup_border_plane(self):
        self.blender.setup_border_planes(2, 2)
        self.assertEqual(self.blender.get_model("border_1").dimensions.y, 2)
        self.assertEqual(self.blender.get_model("border_2").dimensions.y, 2)
        self.assertEqual(self.blender.get_model("border_3").dimensions.y, 2)
        self.assertEqual(self.blender.get_model("border_4").dimensions.y, 2)

    def test_select_objects(self):
        self.import_testing_object()
        self.blender.select_objects(["Camera"])
        self.assertEqual(True, bpy.data.objects[1].select_get())
        self.assertEqual(False, bpy.data.objects["Camera"].select_get())

    def test_setup_bodies(self):
        self.import_testing_object()
        self.blender.activate_model(bpy.data.objects[1])
        self.blender.setup_bodies()
        self.assertEqual(bpy.data.objects[1].rigid_body, bpy.context.object.rigid_body)

    def test_simulate(self):
        self.blender.simulate(50)
        # From 0 up and including 49 = 50
        self.assertEqual(49, bpy.context.scene.frame_current)

    def test_render(self):
        self.blender.render("./tmp", "", "test.png")
        self.assertEqual(True, Path('./tmp/test.png').is_file())

    def test_export_scene(self):
        self.import_testing_object()
        self.blender.export_scene("./tmp/test.obj")
        self.assertEqual(True, Path('./tmp/test.obj').is_file())
        self.assertEqual(True, Path('./tmp/test.mtl').is_file())


if __name__ == '__main__':
    sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    # Parser is only needed when you need to pass commandline options to your script.
    parser = argparse.ArgumentParser()
    parser.add_argument('--testdir', required=True)
    args, remaining = parser.parse_known_args()
    # if you do not need a parser, then skip until here. The Next line is important:
    unittest.main(argv=sys.argv[0:1] + remaining)
