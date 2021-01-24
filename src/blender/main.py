import sys
import pathlib
import random
import time

src_dir = "/workdir"
sys.path.insert(1, src_dir)
time_data = {}

from src.util.parser import Parser  # noqa: E402
from src.util.annotate import write_file  # noqa: E402
from src.blender.scene import Scene  # noqa: E402
from src.blender.object import Object  # noqa: E402
from src.blender.crush import Crush  # noqa: E402


# Main method of our code.
# Sets the paths of background and object.
def main(args):  # noqa: CFQ001
    """
    Main method of our code.
    Sets the paths of background and object.
    :param args: arguments used for parsing to values.
    :return: time_data: a dictionary with timestamps of the different stages of the pipeline
    """
    total_start_time = time.time()

    parser = Parser()

    # Load the config file for camera and lights
    configuration = parser.parse_long_term_configuration(pathlib.Path(
        src_dir + r"/configuration.yaml"))

    # Parse arguments provided as input by user
    args = parser.parse_args(args)

    # Load objects
    if args.reuse_crushes:
        material_dirs = list(map(lambda x: list(pathlib.Path(src_dir + r'/Crushed Models/' +
                                                             x).glob('**/*.obj')), args.materials))
    else:
        material_dirs = list(map(lambda x: list(pathlib.Path(src_dir + r'/Models/' + x).glob(
            '**/*.obj')), args.materials))

    # List of the models
    models = [list(map(lambda path: Object(str(
        path), 'random', 'random', 'random', None), material)) for material in material_dirs]

    # Calculate number of objects per material based on proportions
    number_of_objects = list(map(lambda x: int(round(
        args.objects_per_image * (x / 100))), args.proportions))

    objects = make_object_selection(args, number_of_objects, models)

    if not args.only_crush:
        # Setup scene
        scene = Scene(configuration['camera']['location'], configuration['camera']['rotation'],
                      configuration['light']['location'], configuration['light']['energy'],
                      configuration['light']['type'])
        scene.add_background(args.background, None)

        # Render images
        image_object_bboxes = render(args, configuration['render'], scene, objects)

        # Write info file
        write_file(configuration['info_json'],
                   (configuration['render']['res_width'], configuration['render']['res_height']),
                   'info', args.image_count, image_object_bboxes)

    time_data['total'] = time.time() - total_start_time

    # Print time data
    print('Total Time: ' + str(time_data['total']))
    print('Object Creation Time: ' + str(time_data['object_creation_time']))
    if not args.only_crush:
        print('Object Setup Time: ' + str(time_data['object_setup_time']))
        for i in range(args.image_count):
            print('Image ' + str(i) + ' Time: ' + str(time_data['image_' + str(i)]))

    # To be displayed on the server page
    return time_data


def render(args, render_configuration, scene, objects):
    """
    This method renders images with a static set of objects.
    It first makes random selection of models to be rendered.
    For each image it re-uses the objects but randomizes and repositions them.
    This makes for better performance since we reduce the imports
    form a linear to a constant time complexity.
    :param args: Arguments passed to the main
    :param render_configuration: Current render configuration
    :param scene: Scene containing the background and border planes
    :param objects: Objects to be rendered.
    :return: time_data: for analyzing performance
    """
    # Set render output parameters
    scene.set_render_parameters()
    # Setup scene by making a selection of objects and importing them
    starting_time = time.time()
    scene.clear_scene(['background', 'border_1', 'border_2', 'border_3', 'border_4'])
    for obj in objects:
        scene.add_object(obj)
    scene.setup_bodies()  # Make models rigid bodies
    time_data['object_setup_time'], image_object_bboxes = time.time() - starting_time, []
    for i in range(args.image_count):
        starting_time = time.time()
        scene.reset_objects()
        image_object_bboxes.append(scene.get_labeled_bounding_boxes(render_configuration))
        scene.render_scene(args.output_location, str(i))
        time_data['image_' + str(i)] = time.time() - starting_time
    return image_object_bboxes


def make_object_selection(args, number_of_objects, models):  # noqa: CFQ001
    """
    Makes a random selection of objects that will be used in the scene with proper proportions.
    Checks if their needs to be a new crushing of objects or we will re-use.
    :param args: Arguments passed to the main
    :param number_of_objects: List with proportions to indicate the amount of material objects
    :param models: list of models
    :return: list of selected objects
    """
    starting_time = time.time()
    objects = list()
    if not (args.reuse_crushes or args.dont_crush):
        crusher = Crush()
    for j, number in enumerate(number_of_objects):
        for _ in range(number):
            object_to_add = random.choice(models[j])  # Random choice out of models of material j
            object_to_add.randomize_object(None)
            object_to_add.randomize_skin(object_to_add)
            # Crush model
            if args.reuse_crushes or args.dont_crush:
                objects.append(object_to_add)
            else:
                objects.append(crusher.crush_model(object_to_add, "Crushed Models/"))

    time_data['object_creation_time'] = time.time() - starting_time
    return objects


if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if '.py' in arg:
            main(sys.argv[i + 2:])
