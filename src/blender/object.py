import numpy as np
import os
import random
import pathlib
import sys

sys.path.append(os.getcwd())
src_dir = "/workdir"
sys.path.insert(1, src_dir)

import src.blender.blender as b  # noqa: E402
from src.util.parser import Parser  # noqa: E402

configuration = "configuration.yaml"


class Object:
    """
    Object class to divide logic between an object and blender.
    """

    def __init__(self, path, location, orientation, color, seed):
        """
        Initializes properties of the object.
        :param path: string path specifying object path.
        :param location: string specifying objects location or 'random' for random location.
        :param orientation: string specifying objects orientation or 'random'
        for random orientation.
        :param color: string specifying objects color or 'random' for random color.
        :seed: integer for predictable randomness or None for actual randomness
        """
        self.path = path
        if self.path is not None:
            self.material = str(pathlib.Path(path).parent.stem)
        if location != 'random':
            self.rand_location, self.location = False, location
        else:
            self.rand_location, self.location = True, self.random_location(seed)
        if orientation != 'random':
            self.rand_orientation, self.orientation = False, orientation
        else:
            self.rand_orientation, self.orientation = True, self.random_orientation(seed)
        if color != 'random':
            self.rand_color, self.color = False, color
        else:
            self.rand_color, self.color = True, self.random_color(seed)

    def randomize_object(self, seed):
        """
        If user selects properties of object can be made random
        :param seed: integer for repeatable randomness.
        :return: none
        """
        if self.rand_location:
            self.location = self.random_location(seed)
        if self.rand_orientation:
            self.orientation = self.random_orientation(seed)
        if self.rand_color:
            self.color = self.random_color(seed)

    def random_location(self, seed):
        """
        Return random location.
        :param seed: integer for repeatable randomness.
        :return: 3 entry list to indicate location
        """
        np.random.seed(seed)
        locations = np.random.uniform(low=-0.5, high=0.5, size=2)
        return np.append(locations, 1)

    def random_orientation(self, seed):
        """
        Return random orientation
        :param seed: integer for repeatable randomness.
        :return: 3 entry list to indicate orientation
        """
        np.random.seed(seed)
        rotations = np.random.uniform(low=0, high=360, size=3) * np.pi / 180
        return rotations

    def random_color(self, seed):
        """
        Return random color
        :param seed: integer for repeatable randomness.
        :return: n4 entry list to indicate rgba
        """
        np.random.seed(seed)
        colors = np.random.uniform(low=0.0, high=1.0, size=4)
        return colors

    def randomize_skin(self, obj):
        """
        :param obj: Object whose skin will be changed
        Randomizes skins using skins stored in config file by editing the mtl file.
        :return: None
        """
        # Find path of mtl file
        model_directory = os.path.splitext(self.path)
        mtl_directory = model_directory[0] + '.mtl'

        object_name = os.path.basename(model_directory[0]).split('.')[0]
        material_name = os.path.basename(os.path.dirname(mtl_directory))

        # Read skins from config file
        skins = self.read_skins_from_library()

        # Check if material exists and object is a type of material and exists in config file
        if material_name in skins and object_name in skins[material_name]:
            # Find new skin and change file
            new_skin = random.choice(skins[material_name][object_name])
            self.change_skin(obj, object_name, mtl_directory, new_skin)

    def change_skin(self, obj, object_name, mtl_directory, new_skin):
        """
        Find line number(s) to be changed and change them.
        :param obj: Object whose skin will be changed
        :param mtl_directory: Directory of mtl file to be edited
        :param object_name: object whose skin will be randomized
        :param new_skin: New skin of object
        :return: None
        """
        # Read change_skin from config file
        change_skin_dict = Parser().parse_long_term_configuration(
            pathlib.Path(configuration))['change_skin']
        number = self.get_key(object_name, change_skin_dict)
        if number == 0:
            p = Parser().parse_long_term_configuration(
                pathlib.Path(configuration))['jazz']
            chance = np.random.rand()
            if 1 - p < chance:
                rgba = self.random_color(chance)
                b.Blender().color_object(obj, rgba)

        # Change skins at specified line numbers
        elif number is not None:
            for i in range(int(number)):
                self.change_mtl(mtl_directory, new_skin, 12 + 11 * i)

    def get_key(self, val, my_dict):
        """
        Find key in a dict using value.
        :param val: Value of key to be found
        :param my_dict: Dict to be queried
        :return: Key if found else None
        """
        for key, value in my_dict.items():
            if val in value:
                return key

        return None

    def change_mtl(self, file_to_edit, new_skin, line_number):
        """
        Changes the map_Kd line in mtl file.
        :param line_number: Line number of mtl file to be edited
        :param file_to_edit: File containing line to be changed
        :param new_skin: New line to replace file
        :return: None
        """
        # Read and replace line mtl file
        with open(file_to_edit, 'r') as file:
            data = file.readlines()
            data[line_number] = 'map_Kd ' + new_skin + '\n'

        # Write back to mtl file
        with open(file_to_edit, 'w') as file:
            file.writelines(data)

    def read_skins_from_library(self):
        """
        Read skins from the config file.
        :return: Dict with skins
        """
        return Parser().parse_long_term_configuration(pathlib.Path(configuration))['skins']
