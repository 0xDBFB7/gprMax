# Copyright (C) 2015-2020: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

from copy import deepcopy

import numpy as np

from gprMax.constants import c
from gprMax.constants import floattype
from gprMax.grid import Ix
from gprMax.grid import Iy
from gprMax.grid import Iz
from gprMax.utilities import round_value


class LumpedPort(object):
    '''
    Each port can only be part of one Component.
    '''
    def __init__(self):

        self.SPICE_net_ID = None
        self.xcoord = None
        self.ycoord = None
        self.zcoord = None
        self.polarisation = None
        self.conductor_contour_distance_x = None
        self.conductor_contour_distance_y = None
        self.conductor_contour_distance_z = None

        self.voltage = []
        self.voltage = []

        self.voltage_history = []
        self.current_history = []

def e_field_integrate(G, positive_port, reference_port):
    '''
    Determine the potential difference between two ports.

    Doesn't matter how you integrate.

    '''
    potential_difference = 0
    if(positive_port.xcoord > reference_port.xcoord):
        step = -1
    else:
        step = 1
    for x in range(positive_port.xcoord,reference_port.xcoord, step):
        potential_difference += G.Ex[x, positive_port.ycoord, positive_port.zcoord] * G.dx * step

    if(positive_port.ycoord > reference_port.ycoord):
        step = -1
    else:
        step = 1
    for y in range(positive_port.ycoord,reference_port.ycoord, step):
        potential_difference += G.Ey[positive_port.xcoord, y , positive_port.zcoord] * G.dy * step

    if(positive_port.zcoord > reference_port.zcoord):
        step = -1
    else:
        step = 1
    for z in range(positive_port.zcoord,reference_port.zcoord, step):
        potential_difference += G.Ez[positive_port.xcoord, positive_port.ycoord, z] * G.dz * step

    return potential_difference



class LumpedComponent(object):
    """


    #waveform: gaussiandot 1 1e9 myWave
    #hertzian_dipole: z 0.050 0.050 0.050 myWave

    fields_outputs -> store_outputs

    for tl in G.transmissionlines:
        tl.Vtotal[iteration] = tl.voltage[tl.antpos]
        tl.Itotal[iteration] = tl.current[tl.antpos]


    See "The use of SPICE lumped circuits as sub-grid models for FDTD analysis", doi:10.1109/75.289516
    which deals with lumped elements of a single-cell size, and
    "Incorporating non-linear lumped elements in FDTD: the equivalent source method"
    which deals with objects of arbitrary size.

    You can use this 'equivalent source method' either by line-integrating the currents around a conductor
    and setting the electric field, or by line-integrating the voltage and setting the magnetic field.

    I chose the latter because it seems to make more sense to set a voltage initial-condition in SPICE than a current.

    1. Normal electric field update.
    2. Obtain terminal voltages by an electric field line integration from one port to another.
    3. Normal magnetic field update.  - I think this can happen at any time, actually.
    4. Obtain the lumped currents from the voltages - either via SPICE or via analytic expressions for each component
    5. Set H along a contour enclosing the conductor to net_current / Lc
    6. ...
    7. Profit!



    """

    reference_port = None
    ports = []

    def compute_voltages(self):
        for port in self.ports:
            port.voltage = e_field_integrate(G, port, self.reference_port)
            port.voltage_history.append(port.voltage)

    # def run_spice(self):
        # port.current = e_field_integrate(G, port, self.reference_port)



    #
    #
    # i = self.xcoord
    # j = self.ycoord
    # k = self.zcoord
    #
    #
    # self.voltage
    # self.current
    #
    # if self.polarisation == 'x':
    #     Ex[i, j, k] -= updatecoeffsE[ID[G.IDlookup[componentID], i, j, k], 4] * self.waveformvaluesJ[iteration] * self.dl * (1 / (G.dx * G.dy * G.dz))
    #
    # elif self.polarisation == 'y':
    #     Ey[i, j, k] -= updatecoeffsE[ID[G.IDlookup[componentID], i, j, k], 4] * self.waveformvaluesJ[iteration] * self.dl * (1 / (G.dx * G.dy * G.dz))
    #
    # elif self.polarisation == 'z':
    #     Ez[i, j, k] -= updatecoeffsE[ID[G.IDlookup[componentID], i, j, k], 4] * self.waveformvaluesJ[iteration] * self.dl * (1 / (G.dx * G.dy * G.dz))
    #
    #
    #
    # total_current = (Ix(i, j, k, G.Hx, G.Hy, G.Hz, G)**2.0)
    #                 + (Iy(i, j, k, G.Hx, G.Hy, G.Hz, G)**2.0)
    #                 + (Iz(i, j, k, G.Hx, G.Hy, G.Hz, G)**2.0)
    # total_current = sqrt(total_current)
    #
    # self.current
