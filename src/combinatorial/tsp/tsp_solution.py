#  tsp_solution.py
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
from random import randrange, shuffle
from typing import List

from combinatorial.solution import Solution
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.k_opt import two_opt


class TspSolution(Solution):

  def __init__(self, tsp: Tsp, tour: List[int] = None):
    """
    Create a solution to TSP.

    :param tsp: Instance of TSP
    :param tour: Initial tour, which must end with node 0. If it's null, then a solution is generated
    """
    if tour is None:
      tour = [u for u in range(1, tsp.get_n())]
      shuffle(tour)

    self.tsp = tsp
    self.tour = tour
    self._evaluate_fitness()
    self.validate()

  def get_instance(self):
    return self.tsp

  def get_fitness(self):
    """
    Return current fitness.

    :return: Current fitness
    """
    return self.fitness

  def get_solution(self):
    """
    Return current solution tour.

    To make solution unique, the first node is less than the last node before depot.

    :return: Current tour
    """
    return self.tour if self.tour[0] < self.tour[-2] else self.tour[-2::-1] + [0]

  @staticmethod
  def grasp(instance: Tsp, alpha: float, seed: int = None):
    # FIXME: implement GRASP algorithm
    raise NotImplementedError("GRASP algorithm wasn't implemented for TSP")

  def neighbor(self):
    """
    Search for another solution closer to current one.

    :return: A new solution, which is based on current one
    """
    i = randrange(0, self.tsp.get_n() - 2)
    j = randrange(i + 2, self.tsp.get_n())
    return TspSolution(self.tsp, self.tour[:i] + self.tour[i: j][::-1] + self.tour[j:])

  def local_search(self):
    """
    Move current solution around it trying to improve it.

    :return: None
    """
    self.fitness -= two_opt(self.tour, self.tsp.cost)
    self.validate()

  def _evaluate_fitness(self):
    self.fitness = sum(self.tsp.cost(self.tour[i - 1], self.tour[i]) for i in range(self.tsp.get_n()))

  # noinspection PyUnreachableCode
  def validate(self):
    """
    Abort if current state of solution is invalid.

    :return: None
    """
    if __debug__:
      tsp = self.tsp
      tour = self.tour
      n = tsp.get_n()

      assert tsp is not None
      assert tour is not None
      assert tour[-1] == 0, "Last node must be 0, found {}".format(tour[-1])
      assert min(tour) >= 0, "Invalid node found: {} < 0".format(min(tour))
      assert max(tour) < n, "Invalid node found: {} >= {}".format(max(tour), n)
      assert len(tour) == n, "Invalid tour length: {} != {}".format(len(tour), n)
      assert len(set(tour)) == len(tour), "Duplicates in tour"

      expected_fitness = sum(tsp.cost(tour[i - 1], tour[i]) for i in range(n))
      assert self.fitness == expected_fitness, "Wrong fitness value: {} != {}".format(self.fitness, expected_fitness)
