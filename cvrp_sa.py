#  cvrp_sa.py
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

import sys

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_solution import CvrpSolution
from combinatorial.simulated_annealing import SimulatedAnnealing
from run_tests import run

if __name__ == "__main__":
  instance = Cvrp.read(sys.argv[1][2:])
  repeat = 5
  sa = SimulatedAnnealing.build(start_temperature=10, min_temperature=1, alpha=.999)
  run(instance, CvrpSolution, repeat, sa)
