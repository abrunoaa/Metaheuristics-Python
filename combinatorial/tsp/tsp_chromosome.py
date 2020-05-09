#  tsp_chromosome.py
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
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.tsp_solution import TspSolution


class TspChromosome(Chromosome, TspSolution):
  """
  Chromosome used by Genetic Algorithm for TSP.
  """

  def __init__(self, tsp: Tsp, tour: list = None):
    """
    Create a chromosome with an instance of CVRP.

    :param tsp: Instance to build.
    :param tour: Initial tour, which it's generated if equals None.
    """
    super().__init__(tsp, tour)

  def mate(self, other: 'TspChromosome') -> 'TspChromosome':
    """
    Mate this solution with other.

    Current implementation splits the solutions in two, concatenating first half with second one.
    Of course, there will be duplicates. Nodes in first tour which doesn't occur in second will
    be placed right after first, followed by nodes in second tour if they aren't inserted yet.

    Example (the pipe | indicates the split position, which is randomly generated):
        1 2 3 | 4 5 6 7 => first tour

        1 3 7 | 5 2 6 4 => second tour

        1 2 3 | 5 2 6 4 => 2 appear twice while 7 doesn't appear

        1 2 3 7 | 5 6 4 => insert missing nodes and remove duplicates.

    :param other: Solution to mate with.
    :return: A new solution based on this and other.
    """
    tour1 = self.tour
    tour2 = other.tour
    k = randrange(0, self.tsp.get_n() - 1)

    inserted = set(tour1[: k])
    to_insert = set(v for v in tour2[k:] if v not in inserted)

    new_tour = tour1[: k] + [v for v in tour1[k:] if v not in to_insert] + [v for v in tour2[k:] if v in to_insert]
    return TspChromosome(self.tsp, new_tour)

  def mutate(self) -> None:
    """
    Change this solution in a randomly way.
    Current implementation only reverses a range.

    :return: None.
    """
    cost = self.tsp.cost

    i = randrange(0, self.tsp.get_n() - 2)
    j = randrange(i + 2, self.tsp.get_n())

    self.fitness -= cost(self.tour[i - 1], self.tour[i]) + cost(self.tour[j - 1], self.tour[j])
    self.tour[i: j] = self.tour[i: j][::-1]
    self.fitness += cost(self.tour[i - 1], self.tour[i]) + cost(self.tour[j - 1], self.tour[j])
    self.validate()
