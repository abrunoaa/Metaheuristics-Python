#  crp.py
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
from typing import Tuple, List

from combinatorial.instance import Instance


class Crp(Instance):
  """
  Instance of Cable Routing Problem (CRP).
  """

  MIN_TURBINES = 3

  def __init__(self,
               c: int,
               substation: Tuple[int, int],
               turbines: List[Tuple[int, int]],
               cable_capacity: List[int],
               cable_cost: List[int]):
    # TODO: add documentation

    assert c >= 1, "c must be at least 1"
    assert len(turbines) >= Crp.MIN_TURBINES, "Expected at least {} turbines".format(Crp.MIN_TURBINES)
    assert len(cable_capacity) >= 1, "Expected at least one cable"
    assert len(cable_capacity) == len(cable_cost), "capacity and cost have different sizes"

    self.n = len(turbines)
    self.c = c
    self.turbines = turbines + [substation]
    self.cable_capacity = cable_capacity
    self.cable_cost = cable_cost

  def get_best(self):
    return None

  def get_n(self):
    """
    Returns the number of turbines, which doesn't include the substation.

    :return: Number of turbines.
    """
    return self.n

  def get_locations(self):
    return self.turbines

  def cost(self, u: int, v: int):
    """
    Cost to travel from u to v. Node n means the substation.

    The cost is 2D distance, rounded to nearest integer.

    :param u: Node from graph.
    :param v: Node from graph.
    :return: The cost to travel from u to v.
    """
    diff = lambda i: self.turbines[u][i] - self.turbines[v][i]
    a = diff(0)
    b = diff(1)
    return sqrt(a * a + b * b)

  def choose_cable(self, energy):
    return next(i for i, capacity in enumerate(self.cable_capacity) if energy <= capacity)

  def choose_cable_cost(self, energy):
    assert energy <= self.cable_capacity[-1], "Invalid energy: {} > {}".format(energy, self.cable_capacity[-1])
    return self.cable_cost[self.choose_cable(energy)]

  @staticmethod
  def read(reader):
    """
    Read an instance from a reader.

    The reader must have the following info (square brackets are just comments):

    [number of turbines] n [number of cables] t [max connections to substation] c

    [substation] x y

    [n lines with turbines location] x y

    [t lines with cables info] [supported turbines] k [cost] u

    :param reader: Stream to read from.
    :return: A CRP instance.
    """
    content = [x.strip().split() for x in reader.readlines()]

    n, t, c = map(int, content[0])
    substation = tuple(map(int, content[1]))
    turbines = list(tuple(map(int, content[i])) for i in range(2, n + 2))
    cables = list(tuple(map(int, content[i])) for i in range(n + 2, n + 2 + t))
    k, u = tuple(zip(*cables))

    return Crp(c, substation, turbines, k, u)
