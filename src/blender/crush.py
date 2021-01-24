import src.blender.blender as b  # noqa: E402
import src.blender.object as o  # noqa: E402


class Crush:

    def __init__(self):
        self.blender = b.Blender()

    def crush_model(self, obj, folder):
        """
        Executes all the different stages of the crushing in the right order.
        :param obj: object that gets crushed
        :param folder: for where the model needs to be stored
        :return: Object that references to the location of the crushed model
        """
        # Clear scene
        self.blender.clear_scene([])
        # Setup plane
        self.blender.setup_crush_plane()
        # Import model into scene
        model = self.blender.setup_object(obj)
        # Setup cage for deformation
        self.setup_cage(model)
        # Simulate for frames
        self.blender.simulate(20)
        # Export model
        self.export_model(model, folder + obj.material + "/")

        return o.Object(folder + obj.material + "/" + model.name + ".obj",
                        'random', 'random', 'random', None)

    def setup_cage(self, model):
        """
        Applies all the necessary modifiers to the right objects
        :param model: reference to the target model to which the cage needs to be modeled
        :return: none
        """
        # Set up cage by importing sphere and applying ShrinkWrap modifier
        self.blender.setup_cage(model)
        # Bind model to cage using a MeshDeform modifier
        self.blender.activate_model(model)
        self.blender.set_mesh_deform(self.blender.get_model("Sphere"))
        # Add crushing physics using SoftBody modifier
        self.blender.activate_model(self.blender.get_model("Sphere"))
        self.blender.set_softbody()

    def export_model(self, model, folder):
        """
        Applies the deformation of the model and clears the rest of the scene.
        It then centers the object and exports it as an object.
        :param folder: for where the model needs to be stored
        :param model: The model that needs to be exported
        :return: none
        """
        # Apply deformation
        self.blender.activate_model(model)
        self.blender.apply_modifier("MeshDeform")
        # Set to origin
        self.blender.set_object_location(model, [0, 0, 1])
        # Clear out screen
        self.blender.clear_scene([model.name])
        # Export object
        self.blender.export_scene(folder + model.name + ".obj")
