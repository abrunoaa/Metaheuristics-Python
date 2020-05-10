#  pso_test.py
#
#  Copyright (c) 2020 Bruno Almêda de Oliveira <abrunoaa@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

from continuous.pso import pso
from continuous.run_tests import run
from continuous.functions import *


def call(function, interval):
  w = .5
  c1 = .666
  c2 = .333
  n_particles = 25
  return pso(function, interval, w, c1, c2, n_particles, 1000)


# debugging
if __name__ == "__main__":
  f = easom
  run(100, call, f[1], f[0])
