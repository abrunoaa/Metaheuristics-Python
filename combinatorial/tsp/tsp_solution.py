#  tsp_solution.py
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

from random import shuffle, randrange
from typing import List, Callable

from combinatorial.solution import Solution
from combinatorial.tsp.tsp import Tsp


class TspSolution(Solution):

  def __init__(self, tsp: Tsp, tour: List[int] = None):
    """
    Create a solution to TSP.

    :param tsp: Instance of TSP
    :param tour: Initial tour, which must end with node 0. If it's null, then a solution is generated
    """
    if tour is None:
      tour = [i for i in range(1, tsp.get_n())]
      shuffle(tour)
      tour += [0]

    assert tsp.get_n() >= 3, "The solution will fail if there are less than 3 nodes"
    assert min(tour) >= 0, "Invalid node: {} < 0".format(min(tour))
    assert max(tour) < tsp.get_n(), "Invalid node: {} >= {}".format(max(tour), tsp.get_n())
    assert len(set(tour)) == tsp.get_n(), "Duplicates found in tour"
    assert tour[-1] == 0, "Last node in tour must be 0"

    self.tsp = tsp
    self.tour = tour
    self.fitness = sum(tsp.cost(tour[i - 1], tour[i]) for i in range(tsp.get_n()))
    self.validate()

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
    assert len(self.tour) == len(self.tour[-2::-1] + [0])
    return self.tour if self.tour[0] < self.tour[-2] else self.tour[-2::-1] + [0]

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
    self.fitness -= TspSolution.two_opt(self.tour, self.tsp.cost)
    self.validate()

  @staticmethod
  def two_opt(tour: List[int], distance: Callable):
    """
    Inplace 2-opt implementation for routing problems.

    If tour is None or len(tour) < 2, the function will simply return 0 without any errors.

    :param tour: A list-like that represents a tour, which will be modified
    :param distance: A function which take as argument two nodes and returns a number representing distance
    :return: The total improvement or 0 if tour is None or len(tour) < 2
    """
    if tour is None or len(tour) < 2:
      return 0
    assert len(set(tour)) == len(tour), "Duplicates found in tour: {}".format(tour)
    assert tour[-1] == 0, "Expected depot at end of tour, found {}".format(tour[-1])

    improve = 0
    n = len(tour)
    while True:
      best = 0
      left = None
      right = None
      dis = [distance(tour[i - 1], tour[i]) for i in range(n)]
      for i in range(-1, n - 3):
        a = tour[i]
        b = tour[i + 1]
        for j in range(i + 2, n - 1):
          c = tour[j]
          d = tour[j + 1]
          reduce = dis[i + 1] + dis[j + 1] - distance(a, c) - distance(b, d)
          if reduce > best:
            best = reduce
            left = i + 1
            right = j

      if best == 0:
        # handle implementation problems
        assert len(set(tour)) == len(tour) and tour[-1] == 0, "Invalid state after execution"
        return improve

      assert left < right
      improve += best
      tour[left: right + 1] = tour[left: right + 1][::-1]
      assert tour[-1] == 0
      assert len(set(tour)) == n

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
      assert tour[-1] == 0, "Last node must be 0"
      assert min(tour) >= 0, "Invalid node found"
      assert max(tour) < n, "Invalid node found"
      assert len(tour) == n, "Invalid tour length"
      assert len(set(tour)) == len(tour), "Duplicates found in tour"

      expected_fitness = sum(tsp.cost(tour[i - 1], tour[i]) for i in range(n))
      assert self.fitness == expected_fitness, "Wrong fitness value"
