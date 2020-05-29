#  tsp_ga.py
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

from combinatorial.genetic_algorithm import GeneticAlgorithm
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.tsp_chromosome import TspChromosome
from run_tests import run_and_print
from stopping.max_iterations import MaxIterations


def population_builder(x):
  pop_size = 30
  return [TspChromosome(x) for _ in range(pop_size)]


if __name__ == "__main__":
  instance = Tsp.read(sys.argv[1])

  tests = 20
  cpus = 7

  sa = GeneticAlgorithm.build(crossover=.9, elitism=.9, mutation=.9, stopping_condition=MaxIterations(100))
  run_and_print(instance, sa, population_builder, tests, cpus)
