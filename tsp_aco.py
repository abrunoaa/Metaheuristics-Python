#  tsp_aco.py
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
#
import sys

from combinatorial.ant_colony import AntColonyOptimization
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.tsp_ant import TspAnt
from run_tests import run_and_print
from stopping.max_iterations import MaxIterations


def ant_population_builder(x):
  pop_size = 30
  return [TspAnt(x) for _ in range(pop_size)]


if __name__ == "__main__":
  instance = Tsp.read(sys.argv[1])

  tests = 20
  cpus = 7

  n = instance.get_n()
  pheromone = AntColonyOptimization.default_pheromone(n)
  aco = AntColonyOptimization.build(pheromone, alpha=1, beta=10, rho=0.5, stopping_condition=MaxIterations(2))
  run_and_print(instance, aco, ant_population_builder, tests, cpus)
