#  cvrp.py
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
from math import sqrt
from typing import List, Tuple

from combinatorial.instance import Instance


class Cvrp(Instance):
  """
  Instance of CVRP.
  """

  def __init__(self,
               n: int,
               capacity: int,
               demand: List[int],
               locations: List[Tuple[int, int]],
               best: int = None,
               best_tour: List[int] = None):
    """
    Create an instance.

    The depot must be node 0, while clients are nodes in the range [1, n].

    :param n: Number of clients (>= 2).
    :param capacity: Capacity of truck (> 0).
    :param demand: Demand of depot (= 0) and of the n clients (> 0).
    :param locations: Location of depot and of the n clients.
    :param best:
    :param best_tour:
    """
    assert n >= 2, "Need at least 2 clients: {} < 2".format(n)
    assert capacity > 0, "Invalid capacity: {}".format(capacity)
    assert len(locations) == n + 1, "Expected {} locations".format(n + 1)
    assert all(len(x) == 2 for x in locations), "Each location must have exactly two coordinates"
    assert len(demand) == n + 1, "Expected {} demands".format(n + 1)
    assert demand[0] == 0, "Depot (node 0) must have demand = 0, but was {}".format(demand[0])
    assert min(demand[1:]) > 0, "Invalid demand: {}".format(min(demand))
    assert max(demand) <= capacity, "Demand doesn't fit on truck: {} > {}".format(max(demand), capacity)

    if best is not None:
      assert best_tour[0] == 0, "Best tour must start at depot"
      assert best_tour[-1] == 0, "Best tour must end in depot"
      assert len(set(best_tour)) == n + 1
      assert all(x >= 0 for x in best_tour)
      assert all(x <= n for x in best_tour)
      assert all(best_tour[i - 1] != best_tour[i] for i in range(1, len(best_tour)))

      visited = set()
      for u in best_tour:
        if u:
          assert u not in visited
          visited.add(u)

    self.n = n
    self.location = locations
    self.capacity = capacity
    self.demand = demand
    self.best = best
    self.best_tour = best_tour

    if self.best:
      expected_best = sum(self.cost(best_tour[i - 1], best_tour[i]) for i in range(len(best_tour)))
      assert expected_best == best, "Invalid optimal value: expected {} but was {}".format(expected_best, best)

  def get_best(self):
    return self.best

  def get_n(self):
    return self.n

  def get_locations(self):
    return self.location

  def cost(self, u: int, v: int):
    """
    Cost to travel from u to v.

    The cost is 2D distance, rounded to nearest integer.

    :param u: Node from graph.
    :param v: Node from graph.
    :return: The cost to travel from u to v.
    """
    a = self.location[u][0] - self.location[v][0]
    b = self.location[u][1] - self.location[v][1]
    return int(sqrt(a * a + b * b) + 0.5)

  def get_capacity(self):
    """
    Return the capacity of the truck.

    :return: Capacity of the truck.
    """
    return self.capacity

  def get_all_demands(self):
    """
    Return the demand of all the clients.
    Note that the demand of depot is returned at index 0, and always has the value of 0.

    :return: A list of demands of all clients.
    """
    return self.demand

  def get_demand(self, u: int):
    """
    Return the demand of one client.

    :param u: Client to check.
    :return: The demand of client u.
    """
    return self.demand[u]

  @staticmethod
  def read(reader):
    """
    Read an instance from a reader.

    The reader must have the format as specified at instances/cvrp/.format.cvrp.

    :param reader: Stream to read from.
    :return: A CVRP instance.
    """
    content = [x.strip().split() for x in reader.readlines()]

    n, c = map(int, content[0])
    demand = list(map(int, content[1]))
    locations = list(tuple(map(int, x)) for x in content[2: n + 2])

    try:
      opt = int(content[n + 2][0])
      opt_tour = list(map(int, content[n + 3]))
    except IndexError:
      opt = None
      opt_tour = None

    # noinspection PyTypeChecker
    cvrp = Cvrp(n - 1, c, demand, locations, opt, opt_tour)

    return cvrp
