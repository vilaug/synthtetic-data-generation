import pathlib
import sys
import unittest
import numpy as np

src_dir = "/workdir"
sys.path.insert(1, src_dir)

from src.blender.object import Object  # noqa: E402


def read_mtl_map_kd(edit_file):
    """
    Helper method to read the line being edited.
    :param edit_file: File to be edited
    :return: Edited line of file
    """
    with open(edit_file, 'r') as file:
        data = file.readlines()
        return data[12]


class ObjectTestCase(unittest.TestCase):
    seed = 420

    def test_normal_setup(self):
        normal_object = Object("name", [1, 2, 3], [4, 5, 6], [7, 8, 9], 420)
        self.assertEqual("name", normal_object.path)
        self.assertEqual([1, 2, 3], normal_object.location)
        self.assertEqual([4, 5, 6], normal_object.orientation)
        self.assertEqual([7, 8, 9], normal_object.color)

    def test_random_location(self):
        random_object = Object("name", 'random', 'random', 'random', 420)
        random_object.randomize_object(420)
        [x, y, z] = random_object.location
        np.random.seed(self.seed)
        self.assertEquals(np.random.uniform(low=-0.5, high=0.5), x)
        self.assertEquals(np.random.uniform(low=-0.5, high=0.5), y)
        self.assertEquals(1, z)

    def test_random_color(self):
        random_object = Object("name", 'random', 'random', 'random', 420)
        random_object.randomize_object(420)
        [r, g, b, a] = random_object.color
        np.random.seed(self.seed)
        self.assertEquals(np.random.uniform(low=0.0, high=1.0), r)
        self.assertEquals(np.random.uniform(low=0.0, high=1.0), g)
        self.assertEquals(np.random.uniform(low=0.0, high=1.0), b)

    def test_random_orientation(self):
        random_object = Object("name", 'random', 'random', 'random', 420)
        random_object.randomize_object(420)
        [x, y, z] = random_object.orientation
        np.random.seed(self.seed)
        self.assertEquals(np.random.uniform(low=0, high=360) * np.pi / 180, x)
        self.assertEquals(np.random.uniform(low=0, high=360) * np.pi / 180, y)
        self.assertEquals(np.random.uniform(low=0, high=360) * np.pi / 180, z)

    def test_change_mtl(self):
        # Create object
        test_object = Object("name", "random", "random", "random", 420)

        # Setup object since it requires an external file to be edited
        file_to_edit = pathlib.Path("./test/test_objects/test_cube.mtl")
        test_object.change_mtl(file_to_edit, "TestDoesNotExist.png", 12)
        # Verify initial map_Kd
        assert read_mtl_map_kd(file_to_edit) == "map_Kd TestDoesNotExist.png\n"

        # Change map_Kd to test and assert
        test_object.change_mtl(file_to_edit, "NewSkin.png", 12)
        assert read_mtl_map_kd(file_to_edit) == "map_Kd NewSkin.png\n"

    def test_randomize_skin(self):
        # Create object
        random_object = Object("./test/test_objects/cube/random_cube.obj",
                               "random", "random", "random", 420)

        # Setup object since it requires an external file to be edited
        file_to_edit = pathlib.Path("./test/test_objects/cube/random_cube.mtl")
        random_object.change_mtl(file_to_edit, "TestDoesNotExist.png", 12)
        # Verify initial map_Kd
        assert read_mtl_map_kd(file_to_edit) == "map_Kd TestDoesNotExist.png\n"

        src_dir = "./test/test_objects/cube"
        random_object.randomize_skin(src_dir)

        assert read_mtl_map_kd(file_to_edit) == 'map_Kd NewSkin.png\n'


if __name__ == '__main__':
    unittest.main(argv=sys.argv[0:1])
