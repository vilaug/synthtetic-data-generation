import bpy
import addon_utils
import numpy as np
import pathlib
import glob

import src.blender.object as o  # noqa: E402
import src.util.parser as p  # noqa: E402


class Blender:
    """
    Interacts with Blender.
    """

    # Empty constructor
    # This class uses Blender
    # built-in functions.
    def __init__(self):
        self.camera = None

    def clear_scene(self, except_objects):
        """
        Clears the scene so that there are no side effects from previous operations.
        except the ones specified.
        :param except_objects: list of object name strings not be removed
        :return: None
        """
        self.select_objects(except_objects)
        bpy.ops.object.delete()

    def setup_camera(self, coordinates, rotation):
        """
        Places camera at inputted coordinates.
        :param coordinates: list with 3 entries specifying x,y,z coordinates.
        :param rotation: list with 3 entries specifying rotation.
        :return: None
        """
        cam = bpy.context.scene.camera
        # Move the camera to specific coordinates
        cam.location = coordinates
        # Rotate the camera to specific orientation
        cam.rotation_euler = rotation
        self.camera = cam

    def setup_light(self, coordinates, energy, type):
        """
        Places light at inputted co-ordinates.
        :param coordinates: list with 3 entries specifying x,y,z coordinates.
        :param energy: integer specifying light strength.
        :param type: string specifying light type.
        :return: None
        """
        light_data = bpy.data.lights['Light']
        light_object = bpy.data.objects['Light']
        light_data.energy = energy  # 1000 by default
        light_data.type = type  # in ['POINT', 'SUN', 'SPOT', 'HEMI', 'AREA']
        light_object.location = coordinates

    def setup_object(self, object):
        """
        Imports the object from variable path.
        :param object: object to be setup.
        :return: None
        """
        # Import the current object (of input material) to the scene
        bpy.ops.import_scene.obj(filepath=object.path)
        obj = bpy.context.selected_objects[0]
        self.set_object_location(obj, object.location)
        self.set_object_orientation(obj, object.orientation)
        # self.color_object(obj, object.color)
        return obj

    def reset_objects(self):
        """
        Resets the objects above the plane.
        :return: none
        """
        self.select_objects(['background', 'border_1', 'border_2', 'border_3', 'border_4'])
        random_object = o.Object(None, 'random', 'random', 'random', None)
        for obj in bpy.context.selected_objects:
            random_object.randomize_object(None)
            self.set_object_location(obj, random_object.location)
            self.set_object_orientation(obj, random_object.orientation)
        #  self.color_object(obj, random_object.color)

    def setup_border_plane(self, axis, translation, name):
        """
        Sets up vertical individual border plane.
        :param axis: list with 3 entries specifying specific axis.
        :param translation: list with 3 entries specifying translation plane.
        :param name: string name for border.
        :return: None
        """
        half_pi = 0.5 * np.pi
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.rigidbody.object_add(type='PASSIVE')
        bpy.ops.transform.rotate(value=half_pi, orient_axis=axis)  # , axis=axis)
        bpy.ops.transform.translate(value=translation)
        bpy.context.active_object.name = name

    def setup_border_planes(self, x_size, y_size):
        """
        Sets up vertical border planes.
        :param x_size: integer stating x_size.
        :param y_size: integer stating y_size.
        :return: None
        """
        self.setup_border_plane('Y', (x_size / 2, 0, 0), 'border_1')
        self.setup_border_plane('Y', (-x_size / 2, 0, 0), 'border_2')
        self.setup_border_plane('X', (0, y_size / 2, 0), 'border_3')
        self.setup_border_plane('X', (0, -y_size / 2, 0), 'border_4')

    def setup_background_plane(self, filename, x_size, y_size, seed):
        """
        Render specific background plane with given name
        :param filename: string name of backgorund to be added.
        :param x_size: integer for x_size.
        :param y_size: integer for y_size.
        :param seed: integer for predicting randomness
        :return: None
        """
        # Automatically enable 'Import-Export: Import images as Planes'
        # addon in Blender
        addon_utils.enable("io_import_images_as_planes")
        filename = self.choose_background(filename, seed)
        bpy.ops.import_image.to_plane(
            shader='SHADELESS',
            files=[{'name': filename}])
        # Make plane passive rigid body so it can hold the bodies
        bpy.ops.rigidbody.object_add(type='PASSIVE')
        plane = bpy.context.active_object
        plane.name = 'background'
        # Scale background to fit in camera
        plane.dimensions = (x_size, y_size, 1)

    def choose_background(self, filename, seed):
        """
        Method used for getting the right background or a random one
        :param filename: string name of file or 'random' for random
        :param seed: integer for predicting randomness
        :return: string name of file
        """
        if seed is not None:
            np.random.seed(seed)
        if filename == 'random':
            path = np.random.choice(glob.glob('/workdir/Backgrounds/*.jpg'))
        else:
            path = '/workdir/Backgrounds/' + filename
        return path

    def setup_crush_plane(self):
        """
        Setup plane for curshing.
        This means adding a collision modifier
        :return: None
        """
        bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
        bpy.ops.object.modifier_add(type='COLLISION')

    def set_object_location(self, obj, location):
        """
        Places object at random coordinates.
        :param obj: object to be moved.
        :param location: list with 3 entries specifying x,y,z coordinates.
        :return: None
        """
        obj.location.x = location[0]
        obj.location.y = location[1]
        obj.location.z = location[2]

    def set_object_orientation(self, obj, orientation):
        """
        Rotates object to a random orientation.
        :param obj: object to be rotated.
        :param orientation: list with 3 entries specifying rotation.
        :return: None
        """
        obj.rotation_euler[0] = orientation[0]
        obj.rotation_euler[1] = orientation[1]
        obj.rotation_euler[2] = orientation[2]

    def select_objects(self, except_objects):
        """
        Select all models except for the names given.
        :param except_objects: list of object name strings to not select
        :return: None
        """
        bpy.ops.object.select_by_type(type='MESH')
        for name in except_objects:
            if bpy.data.objects.get(name) is not None:
                bpy.data.objects[name].select_set(False)

    def activate_model(self, model):
        """
        Activates the model.
        :param model: model to be activated
        :return: None
        """
        bpy.context.view_layer.objects.active = model

    def setup_bodies(self):
        """
        Sets up rigid bodies for simulating fall
        :return: None
        """
        bpy.context.scene.rigidbody_world.steps_per_second = 300
        self.select_objects(['background', 'border_1', 'border_2', 'border_3', 'border_4'])
        objects = bpy.context.selected_objects
        for obj in objects:
            # Add rigid body to object
            self.activate_model(obj)
            bpy.ops.rigidbody.object_add()

    def simulate(self, frames):
        """
        Simulates in blender for a certain amount of frames.
        :param frames: integer amount of frames to simulate
        :return: None
        """
        scene = bpy.data.scenes['Scene']
        scene.frame_set(0)
        for i in range(1, frames):
            scene.frame_set(i)

    def render(self, src_dir, output_location, name):
        """
        Renders image in blender.
        :param src_dir: string for source directory.
        :param output_location: string for output folder.
        :param name: string for name of file.
        :return: None
        """
        # Set render device to GPU instead of CPU
        self.set_render_device('GPU')

        bpy.context.scene.render.filepath = \
            src_dir + '/' + output_location \
            + name

        # Render image
        bpy.ops.render.render(write_still=True)
        print('Rendering done!')

    def set_render_output_parameters(self):
        """
        Sets the render output parameters which it gets from configuration.yaml
        The parameters that will be changed are x and y resolution and percentage,
        max amount of ray tracing bounces, samples, tile size
        and set denoising to True.
        :return: None
        """
        scene = bpy.context.scene
        configuration = p.Parser().parse_long_term_configuration(pathlib.Path(
            '/workdir' + r"/configuration.yaml"))
        scene.render.resolution_x = configuration['render']['res_width']
        scene.render.resolution_y = configuration['render']['res_height']
        scene.render.resolution_percentage = configuration['render']['res_percentage']
        scene.cycles.max_bounces = configuration['render']['max_bounces']
        scene.cycles.samples = configuration['render']['samples']
        scene.render.tile_x = configuration['render']['tile_x']
        scene.render.tile_y = configuration['render']['tile_y']
        scene.view_layers['View Layer'].cycles.use_denoising = True

    def set_render_device(self, device):
        """
        Set render device.
        :param device: device to be used for rendering. Choice: [CPU,GPU].
        :return: None
        """
        bpy.context.scene.cycles.device = device

    def color_object(self, obj, rgba):
        """
        Set color of an object to RGB value.
        :param obj: object to be changed color of.
        :param rgba: list with 4 entries specifying rgb colors and the alpha value.
        :return: None
        """
        mat = bpy.data.materials.new("Color")
        mat.diffuse_color = (rgba[0], rgba[1], rgba[2], rgba[3])
        obj.active_material = mat

    def set_softbody(self):
        """
        Adds the SoftBody modifier to the active object
        This is for the realistic deformation of the object
        :return: None
        """
        bpy.ops.object.modifier_add(type='SOFT_BODY')
        bpy.context.object.modifiers["Softbody"].settings.use_goal = False
        bpy.context.object.modifiers["Softbody"].settings.plastic = 100
        bpy.context.object.modifiers["Softbody"].settings.bend = 1000

    def setup_cage(self, target):
        """
        Adds a cage to a target model.
        The cage is made from a sphere .
        It is made in the right form using the ShrinkWrap modifier.
        :param target: object for which the cage gets formed
        :return: None
        """
        bpy.ops.mesh.primitive_uv_sphere_add(radius=5, location=(0, 0, 0))
        # Subdivide surface of sphere to make for better denting [OPTIONAL]
        bpy.ops.object.modifier_add(type='SUBSURF')
        self.apply_modifier("Subsurf")
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.context.object.modifiers["Shrinkwrap"].target = target
        bpy.context.object.modifiers["Shrinkwrap"].offset = 0.05
        bpy.context.object.modifiers["Shrinkwrap"].show_viewport = False
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")

    def set_mesh_deform(self, target):
        """
        Adds the MeshDeform modifier to the active object.
        This binds all the vertices of the active object to the vertices of the (lower-poly) cage.
        :param target: the cage that the active object is mapped to
        :return: None
        """
        bpy.ops.object.modifier_add(type='MESH_DEFORM')
        bpy.context.object.modifiers["MeshDeform"].object = target
        bpy.context.object.modifiers["MeshDeform"].precision = 3
        bpy.ops.object.meshdeform_bind(modifier="MeshDeform")

    def apply_modifier(self, modifier):
        """
        Applies a modifier of the active object.
        modifier can be one of the following enums:
        ['DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT',
        'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_MIX',
        'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT',
        'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF',
        'TRIANGULATE', 'WELD', 'WIREFRAME', 'ARMATURE', 'CAST', 'CURVE', 'DISPLACE', 'HOOK',
        'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH',
        'CORRECTIVE_SMOOTH', 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH',
        'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'FLUID', 'OCEAN', 'PARTICLE_INSTANCE',
        'PARTICLE_SYSTEM', 'SOFT_BODY', 'SURFACE']
        :param modifier: specifies which one to apply
        :return: None
        """
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier)

    def export_scene(self, filepath):
        """
        Exports the current scene as an object.
        :param filepath: place where the scene is stored as well as the name of the object
        :return: None
        """
        bpy.ops.export_scene.obj(filepath=filepath)

    def get_model(self, name):
        """
        Returns the object by name.
        :param name: identifier of object
        :return: object with name
        """
        return bpy.data.objects[name]

    def get_labeled_object_bounding_boxes(self, object_names, render_configuration):
        """
        Gets the bounding boxes for the objects in the scene.
        :param object_names: list of object names
        :param render_configuration: render configuration
        :return: a list of tuples (object name, bounding box)
        """
        bounding_boxes = []
        bpy.context.view_layer.update()
        for obj in bpy.context.scene.objects:
            if obj.name in object_names:
                bounding_box = self.camera_view_bounds_2d(bpy.context.scene, obj)
                bounding_boxes.append((obj.name.split('.')[0], bounding_box))
        return bounding_boxes

    def camera_view_bounds_2d(self, scene, obj):  # noqa: CFQ001
        """
        Taken from
        blender.stackexchange.com/questions/7198/save-the-2d-bounding-box-of-an-object-in-rendered-image-to-a-text-file

        Returns camera space bounding box of mesh object.

        Negative 'z' value means the point is behind the camera.

        Takes shift-x/y, lens angle and sensor size into account
        as well as perspective/ortho projections.

        :arg scene: Scene to use for frame size.
        :type scene: :class:`bpy.types.Scene`
        :arg obj: Untransformed Mesh.
        :type obj: :class:`bpy.types.Mesh´
        :return: a Box object (call its to_tuple() method to get x, y, width and height)
        :rtype: :class:`Box`
        """
        cam_ob = bpy.context.scene.objects['Camera']
        mat = cam_ob.matrix_world.normalized().inverted()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        mesh_eval = obj.evaluated_get(depsgraph)
        me = mesh_eval.to_mesh()
        me.transform(obj.matrix_world)
        me.transform(mat)

        camera = cam_ob.data
        frame = [-v for v in camera.view_frame(scene=scene)[:3]]
        camera_persp = camera.type != 'ORTHO'

        lx = []
        ly = []

        for v in me.vertices:
            co_local = v.co
            z = -co_local.z

            if camera_persp:
                if z == 0.0:
                    lx.append(0.5)
                    ly.append(0.5)
                # Does it make any sense to drop these?
                # if z <= 0.0:
                #    continue
                else:
                    frame = [(v / (v.z / z)) for v in frame]

            min_x, max_x = frame[1].x, frame[2].x
            min_y, max_y = frame[0].y, frame[1].y

            x = (co_local.x - min_x) / (max_x - min_x)
            y = (co_local.y - min_y) / (max_y - min_y)

            lx.append(x)
            ly.append(y)

        min_x = np.clip(min(lx), 0.0, 1.0)
        max_x = np.clip(max(lx), 0.0, 1.0)
        min_y = np.clip(min(ly), 0.0, 1.0)
        max_y = np.clip(max(ly), 0.0, 1.0)

        mesh_eval.to_mesh_clear()

        r = scene.render
        fac = r.resolution_percentage * 0.01
        dim_x = r.resolution_x * fac
        dim_y = r.resolution_y * fac
        # Sanity check
        if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
            return 0, 0, 0, 0

        return (
            round(min_x * dim_x),  # X
            round(dim_y - max_y * dim_y),  # Y
            round((max_x - min_x) * dim_x),  # Width
            round((max_y - min_y) * dim_y)  # Height
        )

    def get_object_names(self):
        """
        Gets the names of the objects that are currently in the scene.
        :return: a list of object_names
        """
        object_names = []
        for obj in bpy.context.scene.objects:
            if obj.name not in ['background', 'border_1', 'border_2',
                                'border_3', 'border_4', 'Camera', 'Light']:
                object_names.append(obj.name)
        return object_names
