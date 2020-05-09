#  tsp.py
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

from math import sqrt
from typing import List, Tuple

from combinatorial.instance import Instance


class Tsp(Instance):
  """
  Instance of TSP.
  """

  def __init__(self, location: List[Tuple[int, int]]):
    """
    Create an instance of TSP.

    :param location: List of locations (x, y) of each node
    """
    assert len(location) >= 3, "Expected at least 3 nodes"

    self.__n = len(location)
    self.__location = location

  def get_n(self):
    """
    Number of nodes in this instance.

    :return: The number of nodes in this instance
    """
    return self.__n

  def get_locations(self):
    """
    Return the 2D location of all nodes.

    :return: Location of all nodes
    """
    return self.__location

  def cost(self, u: int, v: int) -> int:
    """
    Cost to travel from u to v.

    :param u: Node from graph
    :param v: Node from graph
    :return: The cost to travel from u to v
    """
    diff = lambda i: self.__location[u][i] - self.__location[v][i]
    a = diff(0)
    b = diff(1)
    return int(sqrt(a * a + b * b) + 0.5)

  @staticmethod
  def read(filename: str):
    """
    Read the instance from filename.

    :param filename: File to read instance
    :return: A TSP instance
    """
    with open(filename) as file:
      content = [x.strip().split() for x in file.readlines()]

    c = content.index(["NODE_COORD_SECTION"])
    assert c is not None, "Missing NODE_COORD_SECTION"

    number_of_clients = next(int(x[-1]) for x in content if x[0].startswith("DIMENSION"))
    locations = [(int(x[1]), int(x[2])) for x in content[c + 1: c + number_of_clients + 1]]

    return Tsp(locations)
