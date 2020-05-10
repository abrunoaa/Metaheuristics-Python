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

from collections import Callable
from itertools import accumulate, chain
from random import randrange, shuffle

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.solution import Solution
from combinatorial.tsp.tsp_solution import TspSolution
from util.min_queue import MinQueue


class CvrpSolution(Solution):
  """
  Class to represent a solution of CVRP.
  """

  def __init__(self, cvrp: Cvrp, tour = None):
    """
    Create a new solution for CVRP.

    :param cvrp: Instance that this solution solve.
    :param tour: Starting tour to work with. All nodes must be in range [1, n].
    """
    if tour is None:
      tour = [i for i in range(1, cvrp.get_n() + 1)]
      shuffle(tour)

    assert min(tour) >= 1, "Invalid node: {} < 1".format(min(tour))
    assert max(tour) <= cvrp.get_n(), "Invalid node: {} > {}".format(max(tour), cvrp.get_n())
    assert len(set(tour)) == cvrp.get_n(), "Duplicates found in tour"

    self.cvrp = cvrp
    self.tour = tour
    self.fitness = None
    self.truck = None
    self._evaluate_fitness()

  def get_instance(self):
    return self.cvrp

  def get_fitness(self):
    """
    Cost value of this solution.

    :return: Current cost.
    """
    return self.fitness

  def get_solution(self):
    """
    Create a list of lists, representing the routes.
    The lists are sorted lexicographically to give a way to compare solutions.

    :return: A list of routes with the order of attendance.
    """
    tour = self.tour
    return sorted(tour[i: j + 1] if tour[i] < tour[j] else tour[i: j + 1][::-1] for i, j in self.__truck_ranges())

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
    self.__two_opt()
    self.validate()

  def _evaluate_fitness(self):
    """
    Given a TSP-like solution, calculates the optimal positions for splitting into trucks.
    Used for building fitness and truck list of current solution, given a valid tour.

    This function calls validate.

    :return: None
    """
    cvrp = self.cvrp
    tour = self.tour
    dist = cvrp.cost
    n = cvrp.get_n()

    distances = [dist(tour[i], tour[i + 1]) for i in range(n - 1)]
    split = [dist(tour[i], 0) + dist(0, tour[i + 1]) - distances[i] for i in range(n - 1)]
    path = [None] * n
    used = 0
    best = None
    i = 0
    queue = MinQueue()
    queue.push((0, -1))
    for j in range(n):
      used += cvrp.get_demand(tour[j])
      while used > cvrp.get_capacity():
        used -= cvrp.get_demand(tour[i])
        i += 1
        queue.pop()

      assert i <= j
      best, path[j] = queue.min()
      if j < n - 1:
        queue.push((split[j] + best, j))

    self.fitness = best + dist(0, tour[0]) + sum(distances) + dist(tour[-1], 0)
    self.truck = []
    v = n - 1
    while v != -1:
      self.truck.append(v)
      v = path[v]
    self.truck = self.truck[::-1]
    self.validate()

  def __truck_ranges(self):
    """
    Build truck ranges for easy manipulation.

    :return: A generator with pairs of starting and ending nodes position for each truck.
    """
    yield 0, self.truck[0]
    for i in range(1, len(self.truck)):
      yield self.truck[i - 1] + 1, self.truck[i]

  def __two_opt(self):
    """
    Execute two opt algorithm on current instance.

    :return: None.
    """
    tour = [self.tour[i: j + 1] + [0] for i, j in self.__truck_ranges()]
    improve = CvrpSolution.two_opt(tour, self.cvrp.get_all_demands(), self.cvrp.get_capacity(), self.cvrp.cost)

    self.truck = [x - 1 for x in accumulate(len(t) - 1 for t in tour if len(t) > 1)]
    self.tour = list(chain.from_iterable(x[: -1] for x in tour if len(x) > 1))
    self.fitness -= improve

  @staticmethod
  def two_opt(tour: list, demand: list, capacity: int, cost: Callable):
    """
    Run 2-opt on CVRP solution.

    :param tour: List with routes of Cvrp, each one ending with '0'.
    :param demand: Demand of each client.
    :param capacity: Capacity of truck.
    :param cost: Function of two values u and v that calculates the cost for going from u to v.
    :return: Total improvement and new tour.
    """
    # optimize each route
    improve = sum(TspSolution.two_opt(sub_tour, cost) for sub_tour in tour)

    # exchange routes to be 2-opt
    while True:
      load = [sum(demand[u] for u in sub) for sub in tour]
      ntour = len(tour)
      best = 0
      t1 = t2 = p1 = p2 = op_type = None

      # search for best point
      for p in range(ntour - 1):
        used_p = 0
        for i in range(len(tour[p])):
          a = tour[p][i - 1]
          b = tour[p][i]

          for q in range(p + 1, ntour):
            # combine first half with first half
            used_q = 0
            j = 0
            while j < len(tour[q]) and (load[p] - used_p) + (load[q] - used_q) > capacity:
              used_q += demand[tour[q][j]]
              j += 1
            while j < len(tour[q]) and used_p + used_q <= capacity:
              c = tour[q][j - 1]
              d = tour[q][j]
              reduce = cost(a, b) + cost(c, d) - cost(a, c) - cost(d, b)
              if reduce > best:
                best = reduce
                t1, t2 = p, q
                p1, p2 = i, j
                op_type = 1
              used_q += demand[tour[q][j]]
              j += 1

            # combine first half with second half
            used_q = 0
            j = 0
            while j < len(tour[q]) and used_p + (load[q] - used_q) > capacity:
              used_q += demand[tour[q][j]]
              j += 1
            while j < len(tour[q]) and (load[p] - used_p) + used_q <= capacity:
              c = tour[q][j - 1]
              d = tour[q][j]
              reduce = cost(a, b) + cost(c, d) - cost(a, d) - cost(c, b)
              if reduce > best:
                best = reduce
                t1, t2 = p, q
                p1, p2 = i, j
                op_type = 2
              used_q += demand[tour[q][j]]
              j += 1

          used_p += demand[b]

      if best == 0:
        break
      improve += best
      r1 = tour[t1]
      r2 = tour[t2]
      if op_type == 1:
        tour[t1], tour[t2] = r1[: p1] + r2[: p2][::-1] + [0], r1[p1: -1][::-1] + r2[p2:]
      else:
        tour[t1], tour[t2] = r1[: p1] + r2[p2:], r2[: p2] + r1[p1:]
      assert tour[t1][-1] == 0
      assert tour[t2][-1] == 0
      assert sorted(r1 + r2) == sorted(tour[t1] + tour[t2])

      improve += TspSolution.two_opt(tour[t1], cost)
      improve += TspSolution.two_opt(tour[t2], cost)

    return improve

  # noinspection PyUnreachableCode
  def validate(self):
    """
    Abort if current state of solution is invalid.

    :return: None.
    """
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
      assert len(set(tour)) == n, "Duplicates found in tour"
      assert len(truck) > 0, "Missing truck route"
      assert truck[-1] == n - 1, "Last truck must be the last node on tour"

      expected_fitness = sum(dist(0, tour[i]) + sum(dist(tour[k], tour[k + 1]) for k in range(i, j)) + dist(tour[j], 0)
                             for i, j in self.__truck_ranges())
      assert expected_fitness == self.fitness, \
          "Invalid fitness for current tour: {} != {}".format(expected_fitness, self.fitness)

      heaviest = max(sum(cvrp.get_demand(u) for u in tour[i: j + 1]) for i, j in self.__truck_ranges())
      assert heaviest <= capacity, "Truck has load = {}, while capacity = {}".format(heaviest, capacity)
