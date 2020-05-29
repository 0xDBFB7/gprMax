import sys
import unittest

# http://stackoverflow.com/a/17981937/1942837
from contextlib import contextmanager
from io import StringIO

from gprMax.utilities import *

from gprMax.input_cmd_funcs import *


class integral_tests(unittest.TestCase):
    def assert_(self, out, expected_out):
        self.assertEqual(output, expected_out)



if __name__ == '__main__':
    unittest.main()
