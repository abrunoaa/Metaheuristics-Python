#  cvrp_solution.py
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
from itertools import accumulate, chain
from random import random, randrange
from typing import Generator, List, Tuple

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.optimal_split import optimal_truck_split
from combinatorial.cvrp.two_opt import two_opt
from combinatorial.solution import Solution
from util.float_util import less_eq
from util.random_util import roulette


class CvrpSolution(Solution):
  """
  Class to represent a solution of CVRP.
  """

  def __init__(self, cvrp: Cvrp, tour: List[int] = None):
    """
    Create a new solution for CVRP.

    :param cvrp: Instance that this solution solve.
    :param tour: Starting tour to work with. All nodes must be in range [1, n].
    """
    if tour is None:
      tour = CvrpSolution.grasp(cvrp, random(), randrange(1, cvrp.get_n() + 1))

    self.cvrp = cvrp
    self.tour = tour
    self.fitness = None
    self.truck = None
    self._find_fitness_and_optimal_trucks()

  def get_instance(self):
    return self.cvrp

  def get_fitness(self):
    return self.fitness

  def get_solution(self):
    """
    Create a list of lists, representing the routes.

    The lists are sorted lexicographically to give a way to compare solutions.
    Also, each tour starts with the smallest node in the tour.

    :return: A list of routes with the order of attendance.
    """
    tour = []
    for i, j in self._truck_ranges():
      route = self.tour[i: j + 1]
      if len(route) > 1 and route[0] > route[-1]:
        route = route[:: -1]
      tour.append(route)
    return sorted(tour)

  @staticmethod
  def grasp(instance: Cvrp, alpha: float, seed: int = None):
    n = instance.get_n()
    if seed is None:
      seed = randrange(n) + 1
    if not 1 <= seed <= n:
      raise ValueError("Invalid seed {} not in range [{}, {}]".format(seed, 1, n))

    tour = [seed]
    cl = set(range(1, n + 1))
    cl.remove(seed)
    free = instance.get_capacity()
    while cl:
      lst = [(v, instance.cost(tour[-1], v)) for v in cl if instance.get_demand(v) <= free]
      if not lst:
        free = instance.get_capacity()
        lst = [(v, instance.cost(0, v)) for v in cl]
        assert lst

      mn = min(x[1] for x in lst)
      mx = max(x[1] for x in lst)
      cut = mn + alpha * (mx - mn)
      candidates = [(v, cost) for v, cost in lst if less_eq(cost, cut)]
      assert candidates

      k = 0 if len(candidates) == 1 else roulette(mx - x[1] + 1 for x in candidates)
      v = candidates[k][0]
      assert isinstance(v, int)

      tour.append(v)
      free -= instance.get_demand(v)
      cl.remove(v)
      assert len(tour) + len(cl) == n

    assert len(tour) == n
    return tour

  def neighbor(self):
    """
    Search for another solution closer to current one.

    :return: A new solution, which is based on current one.
    """
    i = randrange(0, self.cvrp.get_n() - 1)
    j = randrange(i + 2, self.cvrp.get_n() + 1)
    return CvrpSolution(self.cvrp, self.tour[:i] + self.tour[i: j][::-1] + self.tour[j:])

  def local_search(self):
    """
    Move current solution around it trying to improve it.

    :return: None
    """
    self._two_opt()
    self.validate()

  def _find_fitness_and_optimal_trucks(self):
    self.fitness, self.truck = optimal_truck_split(self.cvrp, self.tour)
    self.validate()

  def _truck_ranges(self) -> Generator[Tuple[int, int], None, None]:
    """
    Build truck ranges for easy manipulation.
    :return: A generator with pairs of starting and ending (both inclusive) nodes position for each truck.
    """
    yield 0, self.truck[0]
    for i in range(1, len(self.truck)):
      yield self.truck[i - 1] + 1, self.truck[i]

  def _two_opt(self):
    """
    Execute 2-opt algorithm on current instance.
    :return: None.
    """
    tour = [self.tour[i: j + 1] + [0] for i, j in self._truck_ranges()]
    self.fitness -= two_opt(tour, self.cvrp.get_all_demands(), self.cvrp.get_capacity(), self.cvrp.cost)

    self.truck = [x - 1 for x in accumulate(len(t) - 1 for t in tour if len(t) > 1)]
    self.tour = list(chain.from_iterable(x[: -1] for x in tour if len(x) > 1))
    self.validate()

  # noinspection PyUnreachableCode
  def validate(self):
    if __debug__:
      cvrp = self.cvrp
      tour = self.tour
      truck = self.truck
      n = cvrp.get_n()
      capacity = cvrp.get_capacity()
      dist = cvrp.cost

      assert cvrp is not None
      assert self.fitness is not None
      assert tour is not None
      assert truck is not None
      assert len(tour) == n, "Invalid tour length"
      assert min(tour) >= 1, "Invalid node: {} < 1".format(min(tour))
      assert max(tour) <= cvrp.get_n(), "Invalid node: {} > {}".format(max(tour), cvrp.get_n())
      assert len(set(tour)) == n, "Duplicates found in tour"
      assert len(truck) > 0, "Missing truck route"
      assert truck[-1] == n - 1, "Last truck must be the last node on tour"

      expected_fitness = sum(dist(0, tour[i]) + sum(dist(tour[k], tour[k + 1]) for k in range(i, j)) + dist(tour[j], 0)
                             for i, j in self._truck_ranges())
      assert expected_fitness == self.fitness, "Wrong fitness {}, expected {}".format(self.fitness, expected_fitness)

      heaviest = max(sum(cvrp.get_demand(u) for u in tour[i: j + 1]) for i, j in self._truck_ranges())
      assert heaviest <= capacity, "Truck has load = {}, while capacity = {}".format(heaviest, capacity)
