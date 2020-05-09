#  cvrp_chromosome.py
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

from random import randrange

from combinatorial.chromosome import Chromosome
from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_solution import CvrpSolution


class CvrpChromosome(Chromosome, CvrpSolution):
  """
  Chromosome used by Genetic Algorithm for CVRP.
  """

  def __init__(self, cvrp: Cvrp, tour: list = None):
    """
    Create a chromosome with an instance of CVRP.

    :param cvrp: Instance to build.
    :param tour: Initial tour, which it's generated if equals None.
    """
    super().__init__(cvrp, tour)

  def mate(self, other: 'CvrpChromosome') -> 'CvrpChromosome':
    """
    Mate this solution with other.

    See mate of TSP Chromosome for more details.

    :param other: Solution to mate with.
    :return: A new solution based on this and other.
    """
    tour1 = self.tour
    tour2 = other.tour
    k = randrange(0, self.cvrp.get_n() - 1)

    inserted = set(tour1[: k])
    to_insert = set(v for v in tour2[k:] if v not in inserted)

    new_tour = tour1[: k] + [v for v in tour1[k:] if v not in to_insert] + [v for v in tour2[k:] if v in to_insert]
    return CvrpChromosome(self.cvrp, new_tour)

  def mutate(self):
    """
    Change this solution in a randomly way.
    Current implementation only reverses a range.

    :return: None.
    """
    i = randrange(0, self.cvrp.get_n() - 1)
    j = randrange(i + 1, self.cvrp.get_n()) + 1
    self.tour[i: j] = self.tour[i: j][::-1]
    self._optimal_split()
