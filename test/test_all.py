import sys
import glob

src_dir = "/workdir"
sys.path.append(src_dir)
sys.path.append(src_dir + "/coveragepy")

import coverage  # noqa: E402

cov = coverage.Coverage(omit=['src/blender/main.py'])
cov.start()

from test.blender.test_blender import BlenderTestCase  # noqa: E402
from test.blender.test_object import ObjectTestCase  # noqa: E402
from test.blender.test_scene import SceneTestCase  # noqa: E402
from test.blender.test_crush import CrushTestCase  # noqa: E402
from test.util.test_parser import ParserTestCase  # noqa: E402
from test.util.test_annotate import AnnotateTestCase  # noqa: E402
from test.server.test_main import ServerMainTestCase  # noqa: E402
from test.server.test_generate import ServerGenerateTestCase  # noqa: E402

import unittest  # noqa: E402

if __name__ == '__main__':
    suites = []
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(ObjectTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(SceneTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(CrushTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(ParserTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(ServerMainTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(ServerGenerateTestCase))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(AnnotateTestCase))
    all_tests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(all_tests).wasSuccessful()

cov.stop()
cov.save()
cov.html_report(glob.glob('src/*/*.py'))
cov.xml_report(glob.glob('src/*/*.py'))
