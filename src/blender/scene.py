import sys
import math

src_dir = "/workdir"
sys.path.insert(1, src_dir)
from src.blender.blender import Blender  # noqa: E402


class Scene:
    """
    Sets up the scene.
    """

    def __init__(self, camera_location, camera_rotation, light_location, light_energy, light_type):
        """
        Constructor method for a scene.
        :param camera_location: List with 3 entries stating x,y,z coordinates.
        :param camera_rotation: List with 3 entries stating rotation values.
        :param light_location: List with 3 entries stating x,y,z coordinates.
        :param light_energy: Integer for light strength.
        :param light_type: Type of light.
        """
        self.blender = Blender()
        self.camera_location = camera_location
        self.camera_rotation = camera_rotation
        self.light_location = light_location
        self.light_energy = light_energy
        self.light_type = light_type
        self.setup_camera()
        self.setup_light()

    def clear_scene(self, except_objects):
        """
        Clears the scene of all objects except the ones specified.
        :param except_objects: list with names of objects that need to stay
        :return: None
        """
        self.blender.clear_scene(except_objects)

    def setup_camera(self):
        """
        Adds the camera to scene.
        :return: None
        """
        self.blender.setup_camera(self.camera_location, self.camera_rotation)

    def setup_light(self):
        """
        Adds light to scene.
        :return: None
        """
        self.blender.setup_light(self.light_location, self.light_energy, self.light_type)

    def add_background(self, filename, seed):
        """
        Adds background plane to the scene.
        :param filename: String name of file.
        :param seed: integer to predict randomness
        :return: None
        """
        # angle of camera-view in radians
        CAMERA_VIEW_ANGLE = [0.691112, 0.5]
        x_size = math.tan(CAMERA_VIEW_ANGLE[0] / 2) * self.camera_location[2] * 2
        y_size = math.tan(CAMERA_VIEW_ANGLE[1] / 2) * self.camera_location[2] * 2
        self.blender.setup_background_plane(filename, x_size, y_size, seed)
        self.blender.setup_border_planes(x_size, y_size)

    def add_object(self, object):
        """
        Adds an object to scene.
        :param object: Object to be added.
        :return: None
        """
        self.blender.setup_object(object)

    def setup_bodies(self):
        """
        Gives the imported models rigid bodies.
        :return: None
        """
        self.blender.setup_bodies()

    def reset_objects(self):
        """
        Resets the bodies with a random color, location and orientation
        :return: None
        """
        self.blender.reset_objects()

    def render_scene(self, output_location, name):
        """
        Renders the scene.
        :param output_location: String location of output.
        :param name: String name of output image.
        :return: None
        """
        self.blender.simulate(100)
        self.blender.render(src_dir, output_location, name)

    def set_render_parameters(self):
        """
        Set the render output parameters.
        :return: None
        """
        self.blender.set_render_output_parameters()

    def get_labeled_bounding_boxes(self, render_configuration):
        """
        Gets the object bounding boxes for the current scene
        :param render_configuration: configuration for the render
        :return: list of (object name, bounding box)
        """
        object_names = self.blender.get_object_names()
        return self.blender.get_labeled_object_bounding_boxes(object_names, render_configuration)

    def export_scene(self, filepath):
        """
        Export a specific scene as an object
        :param filepath: string path for exported object
        :return: None
        """
        self.blender.export_scene(filepath)
