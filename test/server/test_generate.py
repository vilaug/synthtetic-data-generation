import unittest
import sys

src_dir = "/workdir"
sys.path.insert(1, src_dir)

from src.server import generate  # noqa: E402


class ServerGenerateTestCase(unittest.TestCase):

    def test_check_materials(self):
        materials = ['test', 'test1', 'test3']
        prop = '100'
        form = dict(test=prop, test1='a', test2=None, test3='')
        material_list, material_prop, found_false_input, total_prop \
            = generate.check_materials(form, materials, lambda x, y: None)
        self.assertEqual(materials[0] + ' ', material_list)
        self.assertEqual(material_prop, prop + ' ')
        self.assertTrue(found_false_input)
        self.assertEqual(total_prop, int(prop))

    def test_check_numerical_parameters_good(self):
        object_count = '1'
        image_count = '1'
        numerical_parameters = [['', 'object_count'], ['', 'image_count']]
        form = dict(object_count=object_count, image_count=image_count)
        bash_script, found_false_input = generate.check_numerical_parameters(form, '',
                                                                             lambda x, y: None,
                                                                             numerical_parameters)
        self.assertEquals(f"--object_count={object_count} --image_count={image_count} ",
                          bash_script)
        self.assertFalse(found_false_input)

    def test_check_numerical_parameters_bad_1(self):
        object_count = ''
        image_count = ''
        numerical_parameters = [['', 'object_count'], ['', 'image_count']]
        form = dict(object_count=object_count, image_count=image_count)
        bash_script, found_false_input = generate.check_numerical_parameters(form, '',
                                                                             lambda x, y: None,
                                                                             numerical_parameters)
        self.assertEquals('', bash_script)
        self.assertFalse(found_false_input)

    def test_check_numerical_parameters_bad_3(self):
        object_count = 'a'
        image_count = 'a'
        form = dict(object_count=object_count, image_count=image_count)
        numerical_parameters = [['', 'object_count'], ['', 'image_count']]
        bash_script, found_false_input = generate.check_numerical_parameters(form, '',
                                                                             lambda x, y: None,
                                                                             numerical_parameters)
        self.assertEquals('', bash_script)
        self.assertTrue(found_false_input)

    def test_switch_parameters_good(self):
        switch_parameters = [['', 'test'], ['', 'test1']]
        form = dict(test='')
        bash_script, found_false_input = generate.check_switches(form, '', lambda x, y: None,
                                                                 switch_parameters)
        self.assertEquals('--test 1 ', bash_script)
        self.assertFalse(found_false_input)

    def test_switch_parameters_bad(self):
        switch_parameters = [['', 'test'], ['', 'test1']]
        form = dict(test='', test1='')
        bash_script, found_false_input = generate.check_switches(form, '', lambda x, y: None,
                                                                 switch_parameters)
        self.assertEquals('--test 1 ', bash_script)
        self.assertTrue(found_false_input)

    def test_get_time_data(self):
        output = 'Total Time: 68.92672538757324\n' \
                 'Object Creation Time: 35.33028221130371\n' \
                 'Object Setup Time: 5.924004077911377\n' \
                 'Image 0 Time: 27.30325198173523\n'
        time_data = generate.get_time_data(output)
        self.assertAlmostEqual(time_data['Total time'], 68.92672538757324)
        self.assertAlmostEqual(time_data['Object creation'], 35.33028221130371)
        self.assertAlmostEqual(time_data['Object setup'], 5.924004077911377)
        self.assertAlmostEqual(time_data['Image 0'], 27.30325198173523)
