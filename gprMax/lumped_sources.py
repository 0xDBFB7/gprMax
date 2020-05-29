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



class LumpedComponent(object):
    """



    #waveform: gaussiandot 1 1e9 myWave
    #hertzian_dipole: z 0.050 0.050 0.050 myWave

    fields_outputs -> store_outputs

    for tl in G.transmissionlines:
        tl.Vtotal[iteration] = tl.voltage[tl.antpos]
        tl.Itotal[iteration] = tl.current[tl.antpos]


    See "The use of SPICE lumped circuits as sub-grid models for FDTD analysis", doi:10.1109/75.289516
    "Incorporating non-linear lumped elements in FDTD: the equivalent source method"
    """


    '''
    here's some blather

    The way I've used the sources is as follows:

    ------------------------------------------- - microstrip trace or component lead
                     !                          - source, Z polarized
                    | |                         - copper via
                    | |                         - copper via
    ------------------------------------------- - copper plane
    that way the electric field across the source is approximately equal
    to the voltage across


    this is the method used in [antenna paper].

    it would be much more useful to integrate over the field from some specified
    ground cell to get the relative voltage, especially
    when we're talking about component leads.

    '''

    i = self.xcoord
    j = self.ycoord
    k = self.zcoord


    self.voltage
    self.current

    if self.polarisation == 'x':
        Ex[i, j, k] -= updatecoeffsE[ID[G.IDlookup[componentID], i, j, k], 4] * self.waveformvaluesJ[iteration] * self.dl * (1 / (G.dx * G.dy * G.dz))

    elif self.polarisation == 'y':
        Ey[i, j, k] -= updatecoeffsE[ID[G.IDlookup[componentID], i, j, k], 4] * self.waveformvaluesJ[iteration] * self.dl * (1 / (G.dx * G.dy * G.dz))

    elif self.polarisation == 'z':
        Ez[i, j, k] -= updatecoeffsE[ID[G.IDlookup[componentID], i, j, k], 4] * self.waveformvaluesJ[iteration] * self.dl * (1 / (G.dx * G.dy * G.dz))



    total_current = (Ix(i, j, k, G.Hx, G.Hy, G.Hz, G)**2.0)
                    + (Iy(i, j, k, G.Hx, G.Hy, G.Hz, G)**2.0)
                    + (Iz(i, j, k, G.Hx, G.Hy, G.Hz, G)**2.0)
    total_current = sqrt(total_current)

    self.current
