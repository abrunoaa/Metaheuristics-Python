#  cvrp_ga.py
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

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_chromosome import CvrpChromosome
from combinatorial.genetic_algorithm import GeneticAlgorithm
from run_tests import run_and_print
from stopping.max_iterations import MaxIterations


def population_builder(x):
  population_size = 25
  return [CvrpChromosome(x) for _ in range(population_size)]


if __name__ == "__main__":
  instance = Cvrp.read(sys.argv[1])

  tests = 20
  cpus = 7

  sa = GeneticAlgorithm.build(crossover=.9, elitism=.9, mutation=.9, stopping_condition=MaxIterations(100))
  run_and_print(instance, sa, population_builder, tests, cpus)
