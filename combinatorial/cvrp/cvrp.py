#  cvrp.py
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

from typing import List, Tuple

from combinatorial.instance import Instance


class Cvrp(Instance):
  """
  Instance of CVRP.
  """

  def __init__(self, n: int, capacity: int, demand: List[int], location: List[Tuple[int, int]]):
    """
    Create an instance.

    :param n: Number of clients (>= 2).
    :param capacity: Capacity of truck (> 0).
    :param demand: Demand of depot (= 0) and of the n clients (> 0).
    :param location: Location of depot and of the n clients.
    """
    assert n >= 2, "Need at least 2 clients: {} < 2".format(n)
    assert capacity > 0, "Invalid capacity: {}".format(capacity)
    assert len(location) == n + 1, "Expected {} locations".format(n + 1)
    assert len(demand) == n + 1, "Expected {} demands".format(n + 1)
    assert demand[0] == 0, "Depot (node 0) must have demand = 0, but was {}".format(demand[0])
    assert min(demand[1:]) > 0, "Invalid demand = {}!".format(min(demand))
    assert max(demand) <= capacity, "Demand doesn't fit on truck: {} > {}".format(max(demand), capacity)

    super().__init__(location)
    self.capacity = capacity
    self.demand = demand

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
  def read(filename: str):
    """
    Read an instance from a file.
    The file must have the following info (in any order):
    DIMENSION: [integer n representing the number of clients]
    CAPACITY: [integer c representing the capacity of truck]
    NODE_COORD_SECTION [followed by n+1 lines, each one with the the point] x y
    DEMAND_SECTION [followed by n+1 lines, each one with the demand] d

    :param filename: File to read from.
    :return: An instance with data from file.
    """
    with open(filename) as file:
      content = [x.strip().split() for x in file.readlines()]

    c = content.index(["NODE_COORD_SECTION"])
    d = content.index(["DEMAND_SECTION"])

    assert c is not None, "Missing NODE_COORD_SECTION"
    assert d is not None, "Missing DEMAND_SECTION"

    number_of_clients = next(int(x[-1]) - 1 for x in content if x[0].startswith("DIMENSION"))
    capacity = next(int(x[-1]) for x in content if x[0].startswith("CAPACITY"))
    demand = [int(x[1]) for x in content[d + 1: d + number_of_clients + 2]]
    locations = [(int(x[1]), int(x[2])) for x in content[c + 1: c + number_of_clients + 2]]

    return Cvrp(number_of_clients, capacity, demand, locations)
