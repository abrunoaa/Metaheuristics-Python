#  genetic_algorithm_cvrp.py
#
#  Copyright (c) 2020 Bruno Almeda de Oliveira <abrunoaa@gmail.com>
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

from combinatorial.cvrp.chromosome import Chromosome
from combinatorial.genetic_algorithm import genetic_algorithm

from combinatorial.run_tests import run


def function(cvrp):
  iterations = 100
  crossover = .9
  elitism = .9
  mutation = .9
  pop_size = 30
  return genetic_algorithm(iterations, crossover, elitism, mutation, [Chromosome(cvrp) for _ in range(pop_size)])


# debugging
if __name__ == "__main__":
  # run('A\\A-n32-k5.vrp', 100, function)
  run('X\\X-n256-k16.vrp', 100, function)
