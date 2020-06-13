#  tsp.py
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
from itertools import combinations
from math import sqrt
from typing import List, Tuple

from combinatorial.instance import Instance

try:
  from gurobipy import GRB, Model, quicksum
except ImportError:
  GRB = None
  Model = None
  # noinspection SpellCheckingInspection
  quicksum = None


class Tsp(Instance):
  """
  Instance of TSP.
  """

  def __init__(self, locations: List[Tuple[int, int]]):
    """
    Create an instance of TSP.

    :param locations: List of locations (x, y) of each node
    """
    self.n = len(locations)
    self.locations = locations

  def get_n(self):
    return self.n

  def get_locations(self):
    return self.locations

  def cost(self, u: int, v: int) -> int:
    """
    Cost to travel from u to v.

    :param u: Node from graph.
    :param v: Node from graph.
    :return: The cost to travel from u to v.
    """
    diff = lambda i: self.locations[u][i] - self.locations[v][i]
    a = diff(0)
    b = diff(1)
    return int(sqrt(a * a + b * b) + 0.5)

  @staticmethod
  def read(filename):
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


# noinspection PyProtectedMember,PyArgumentList,PyCallingNonCallable,PyUnresolvedReferences
class TspOptimizer:
  # TODO: document this class

  MIN_OPTIMIZER_NODES = 1
  MAX_OPTIMIZER_NODES = 500
  AVAILABLE = Model is not None
  optimizers = {}

  @staticmethod
  def get_instance(n: int) -> 'TspOptimizer':
    if n not in TspOptimizer.optimizers:
      TspOptimizer.optimizers[n] = TspOptimizer(n)

    return TspOptimizer.optimizers[n]

  def __init__(self, n):
    """
    Builds a Gurobi model to solve TSP with n nodes.

    :param n: Number of nodes.
    """
    if not TspOptimizer.AVAILABLE:
      raise NotImplementedError("Can't use method without Gurobi installed")
    if not TspOptimizer.MIN_OPTIMIZER_NODES <= n <= TspOptimizer.MAX_OPTIMIZER_NODES:
      raise ValueError("Number of nodes {} is out of range [{}, {}]"
                       .format(n, TspOptimizer.MIN_OPTIMIZER_NODES, TspOptimizer.MAX_OPTIMIZER_NODES))

    self.n = n
    self.model = Model()
    self.model.Params.OutputFlag = 0
    self.model.Params.lazyConstraints = 1

    # objective (initially, set objective values to 0)
    self.vars = self.model.addVars(((i, j) for i in range(n) for j in range(i)), vtype=GRB.BINARY, name='g')
    for i, j in self.vars.keys():
      self.vars[j, i] = self.vars[i, j]

    self.model._n = self.n
    self.model._vars = self.vars

    # constraints
    self.model.addConstrs(self.vars.sum(i, '*') == 2 for i in range(n))

  def optimize(self, tsp: Tsp):
    """
    Given a TSP instance, this method call Gurobi to solve it.

    :param tsp: The instance to solve.
    :return: The optimal solution.
    :raises ValueError if the number of nodes in the instance differs from the optimizer.
    """
    if tsp.get_n() != self.n:
      raise ValueError("Optimizer supports exactly {} nodes, but {} was received.".format(self.n, tsp.get_n()))

    # update model's coefficients
    dist = {(i, j): tsp.cost(i, j) for i in range(self.n) for j in range(i)}
    for i, j in dist.keys():
      self.vars[i, j].obj = dist[i, j]

    # solve
    self.model.optimize(self.callback)

    # get the answer
    values = self.model.getAttr('x', self.vars)
    g = TspOptimizer.build_graph(values, self.n)
    tour = TspOptimizer.shortest_tour(g, self.n)
    assert len(tour) == self.n
    return self.model.objVal, tour

  @staticmethod
  def callback(model, where):
    if where == GRB.Callback.MIPSOL:
      # remove sub tour
      values = model.cbGetSolution(model._vars)
      g = TspOptimizer.build_graph(values, model._n)
      tour = TspOptimizer.shortest_tour(g, model._n)
      if len(tour) < model._n:
        model.cbLazy(quicksum(model._vars[i, j] for i, j in combinations(tour, 2)) <= len(tour) - 1)

  @staticmethod
  def shortest_tour(g, n):
    cycle = range(n + 1)
    vis = [0] * n
    for u in range(n):
      if vis[u] == 0:
        cur = []
        v = u
        while vis[v] == 0:
          vis[v] = 1
          cur.append(v)
          v = g[v]
        if u != v:
          print(u, v)
        assert u == v
        if len(cur) < len(cycle):
          cycle = cur
    assert len(cycle) > 0
    return cycle

  @staticmethod
  def build_graph(values, n):
    selected = [[] for _ in range(n)]
    for i, j in values.keys():
      if values[i, j] > .5:
        selected[i].append(j)

    assert len(selected) == n
    assert all(len(neighbor) == 2 for neighbor in selected)
    assert all(v[0] != v[1] for v in selected)
    assert all(sum(v == u for neighbor in selected for v in neighbor) == 2 for u in range(n))

    g = [-1 for _ in range(n)]
    for u in range(n):
      p = -1
      while g[u] == -1:
        for v in selected[u]:
          if v != p:
            # noinspection PyTypeChecker
            g[u] = v
            p = u
            u = v
            break

    assert len(g) == n
    assert all(v != -1 for v in g)
    return g
