import argparse
import yaml


class Parser:
    """
    Used for parsing command line inputs.
    """

    def __init__(self):  # noqa: CFQ001
        """
        Constructor method for specifying default values.
        """
        self.parser_field = argparse.ArgumentParser(description='Generate synthetic data')
        self.parser_field.add_argument('-m', '--materials', nargs='+',
                                       help="a list of materials generated in an image",
                                       default=["Aluminium"])
        self.parser_field.add_argument('-p', '--proportions', nargs='+',
                                       help="a list of proportions for each material specified",
                                       type=int, default=[100])
        self.parser_field.add_argument('-c', '--objects_per_image',
                                       help="number of objects per image", type=int, default=1)
        self.parser_field.add_argument('-i', '--image_count',
                                       help="number of images generated", type=int, default=1)
        self.parser_field.add_argument('-b', '--background', help="name of background image file",
                                       default='random')
        self.parser_field.add_argument('-o', '--output_location',
                                       help="path to image directory", default="images/")
        self.parser_field.add_argument('-rc', '--reuse_crushes',
                                       help="use existing crushed models instead of creating them")
        self.parser_field.add_argument('-oc', '--only_crush',
                                       help="only crush the models of the given material,"
                                            " don't render images")
        self.parser_field.add_argument('-dc', '--dont_crush',
                                       help="don't crush the models")

    def parse_args(self, args):
        """
        Parse the arguments.
        :param args: list with arguments to be parsed.
        :return: list with parsed arguments.
        """
        parsed_args = self.parser_field.parse_args(args)
        self.validate_parsed_args(parsed_args)
        return parsed_args

    def validate_parsed_args(self, parsed_args):
        """
        Validate if parsed arguments are valid.
        :param parsed_args: list with parsed arguments.
        :return: none or error if not valid
        """
        if len(parsed_args.materials) != len(parsed_args.proportions):
            raise OSError('material list and proportions list should be of same size')
        if sum(parsed_args.proportions) != 100:
            raise OSError('proportions list should add up to 100')

    def parse_long_term_configuration(self, name):
        """
        Parse long term configurations from yaml file.
        :name: path to the file with configurations.
        :return: dictionary containing configurations.
        """
        with open(str(name)) as configuration:
            data = yaml.load(configuration, Loader=yaml.Loader)
            return data
