import sys
import unittest

# http://stackoverflow.com/a/17981937/1942837
from contextlib import contextmanager
from io import StringIO

from gprMax.utilities import *

from gprMax.input_cmd_funcs import *
from gprMax.grid import FDTDGrid
from gprMax.lumped_components import *


def create_test_grid():
    G = FDTDGrid()
    G.dx = 0.1
    G.dy = 0.1
    G.dz = 0.1
    G.nx = 10
    G.ny = 10
    G.nz = 10
    G.initialise_geometry_arrays()
    G.initialise_field_arrays()
    return G

class integral_tests(unittest.TestCase):
    def test_E_field_integral(self):
        G = create_test_grid()
        reference_port = LumpedPort()
        reference_port.xcoord = 10
        reference_port.ycoord = 10
        reference_port.zcoord = 10

        positive_port = LumpedPort()
        positive_port.xcoord = 0
        positive_port.ycoord = 0
        positive_port.zcoord = 0

        G.Ex.fill(1) #1 v/m
        voltage = e_field_integrate(G, positive_port, reference_port)
        self.assertAlmostEqual(voltage, 1.0, delta=0.05)

        G.Ex.fill(0) #1 v/m
        G.Ey.fill(1) #1 v/m
        voltage = e_field_integrate(G, positive_port, reference_port)
        self.assertAlmostEqual(voltage, 1.0, delta=0.05)

        G.Ey.fill(0) #1 v/m
        G.Ez.fill(1) #1 v/m
        voltage = e_field_integrate(G, positive_port, reference_port)
        self.assertAlmostEqual(voltage, 1.0, delta=0.05)

# class (unittest.TestCase):


if __name__ == '__main__':
    unittest.main()
