#  crp_solution.py
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
from collections import deque
from copy import copy
from math import atan2
from random import uniform
from typing import List

from combinatorial.crp.crp import Crp
from combinatorial.instance import Instance
from combinatorial.solution import Solution
from util.segment import intersect


class CrpSolution(Solution):
  # TODO: document this class

  def __init__(self, crp: Crp, tree: List[int] = None, fitness: float = None, energy: List[int] = None):
    if tree is None:
      tree = CrpSolution.generate(crp)

    self.crp = crp
    self.tree = tree
    self.go_sub = sum(tree[u] == crp.n for u in range(crp.n))
    self.energy = (energy if energy is not None else self._eval_energy())
    self.fitness = (fitness if fitness is not None else self._eval_fitness())
    self.validate()

  def get_instance(self) -> Crp:
    return self.crp

  def get_fitness(self):
    return self.fitness

  def get_solution(self):
    return self.tree

  @staticmethod
  def grasp(instance: Instance, alpha: float, seed=None):
    # FIXME: implement GRASP algorithm for CRP
    raise NotImplementedError("GRASP wasn't implemented for CRP")

  def _isvalid(self, u: int, v: int):
    """
    Check if disconnecting u from it's parent and connecting to v is a valid exchange.
     
    :param u: Node to disconnect. 
    :param v: New node to connect.
    :return: True if the exchange is valid. False otherwise.
    """
    n = self.crp.n
    tree = self.tree

    # trivial cases
    if u == v:
      return False
    if tree[u] == v:
      return False

    if v == n:
      if self.go_sub == self.crp.c:
        return False
    else:
      # if creates a cycle
      w = v
      while w != u and tree[w] != n:
        w = tree[w]
      if w == u:
        return False

      # if overflow the biggest cable
      if self.energy[u] + self.energy[w] > self.crp.cable_capacity[-1]:
        t = u
        while tree[t] != n:
          t = tree[t]
        if w != t:
          return False

    # if creates intersection
    turbine = self.crp.turbines
    for w in range(n):
      if intersect(turbine[u], turbine[v], turbine[w], turbine[tree[w]]):
        return False

    return True

  def _depth(self, u):
    d = 0
    while u != self.crp.n:
      u = self.tree[u]
      d += 1
    return d

  def _change_in_cost(self, u: int, v: int):
    """
    Calculates the cost to change the parent of u to v.

    Assumes:
      * u != v;
      * tree[u] != v;
      * The cable will not overflow;
      * u is not the parent of v (in any level), i.e., doesn't create cycle.

    :param u: Node to disconnect.
    :param v: New parent of u.
    :return: The cost to change the parent of u to v.
    """
    calc_cost = lambda a, b, e: self.crp.choose_cable_cost(e) * self.crp.cost(a, b)

    tree = self.tree
    previous_energy = self.energy[u]
    cost = calc_cost(u, tree[u], previous_energy) - calc_cost(u, v, previous_energy)

    u = tree[u]
    du, dv = self._depth(u), self._depth(v)
    while du < dv:
      cost += calc_cost(v, tree[v], self.energy[v]) - calc_cost(v, tree[v], self.energy[v] + previous_energy)
      v = tree[v]
      dv -= 1
    while du > dv:
      cost += calc_cost(u, tree[u], self.energy[u]) - calc_cost(u, tree[u], self.energy[u] - previous_energy)
      u = tree[u]
      du -= 1
    while u != v:
      cost += calc_cost(v, tree[v], self.energy[v]) - calc_cost(v, tree[v], self.energy[v] + previous_energy)
      cost += calc_cost(u, tree[u], self.energy[u]) - calc_cost(u, tree[u], self.energy[u] - previous_energy)
      u = tree[u]
      v = tree[v]

    return cost

  def _get_changing_candidates(self):
    n = self.crp.n
    tree = self.tree

    candidates = []
    for u in range(n):
      if tree[u] != n or self.go_sub != 1:
        for v in range(n):
          if self._isvalid(u, v):
            candidates.append((self._change_in_cost(u, v), u, v))
        if self._isvalid(u, n):
          candidates.append((self._change_in_cost(u, n), u, n))

    return candidates

  def _exchange_inplace(self, u: int, p: int):
    v = self.tree[u]
    while v != self.crp.n:
      self.energy[v] -= self.energy[u]
      v = self.tree[v]

    v = p
    while v != self.crp.n:
      self.energy[v] += self.energy[u]
      v = self.tree[v]

    if self.tree[u] == self.crp.n:
      self.go_sub -= 1
    elif p == self.crp.n:
      self.go_sub += 1

    self.tree[u] = p

  def local_search(self):
    n = self.crp.n
    while True:
      candidates = []
      for c in self._get_changing_candidates():
        if c[0] > 0 and (c[2] != n or self.go_sub < n) and (self.go_sub > 1 or self.tree[c[1]] != n):
          candidates.append(c)
      if not candidates:
        break

      change = min(candidates)
      self._exchange_inplace(change[1], change[2])
      self.fitness -= change[0]
      self.validate()

  def neighbor(self):
    candidates = self._get_changing_candidates()
    if not candidates:
      raise RuntimeError("Solution trapped!")

    candidates.sort(reverse=True, key=lambda x: x[0])
    mn = candidates[-1][0] - 1
    r = uniform(0, sum(x[0] - mn for x in candidates) - 1e-12)
    for x in candidates:
      r -= x[0] - mn
      if r <= 0:
        new_tree = copy(self.tree)
        new_tree[x[1]] = x[2]
        assert self.tree != new_tree
        return CrpSolution(self.crp, new_tree, self.fitness - x[0])

    raise RuntimeError("No solutions found!")

  def _eval_energy(self):
    n = self.crp.n

    reach = [0] * (n + 1)
    for u in range(n):
      reach[self.tree[u]] += 1
    assert reach[n] == self.go_sub
    assert min(reach) == 0, "Expected at least one leaf node"

    energy = [1] * n
    q = deque(u for u in range(n) if reach[u] == 0)
    while q:
      u = q.popleft()
      v = self.tree[u]
      if v != n:
        reach[v] -= 1
        energy[v] += energy[u]
        if reach[v] == 0:
          q.append(v)

    assert max(reach[: -1]) == 0, "Some node wasn't explored"
    return energy

  def _eval_fitness(self):
    cost = self.crp.cost
    choose = self.crp.choose_cable_cost
    return sum(cost(u, self.tree[u]) * choose(self.energy[u]) for u in range(self.crp.n))

  # noinspection PyUnreachableCode
  def validate(self) -> None:
    if __debug__:
      n = self.crp.n
      tree = self.tree

      assert len(tree) == n, "Unexpected size of tree: {} != {}".format(len(tree), n)
      vis = [0] * n
      for u in range(n):
        v = u
        while v != n and vis[v] == 0:
          vis[v] = 2
          v = tree[v]
        assert v == n or vis[v] == 1, "Found cycle in the tree"
        v = u
        while v != n and vis[v] == 2:
          vis[v] = 1
          v = tree[v]

      assert self.go_sub >= 1, "Energy doesn't reach substation"
      assert self.go_sub <= self.crp.c, "Limit of connections to substation exceeded"
      assert self.go_sub == sum(tree[u] == n for u in range(n)), "Wrong counter for nodes reaching substation"
      assert self.energy == self._eval_energy(), "Wrong energy values"
      assert sum(self.energy[u] for u in range(n) if tree[u] == n) == n, "Wrong energy calculation"

      fitness_diff = abs(self.fitness - self._eval_fitness()) < 1e-3
      assert fitness_diff, "Wrong fitness {} != {}".format(self.fitness, self._eval_fitness())

  @staticmethod
  def generate(crp: Crp):
    used = 0
    v = -1
    tree = [-1] * crp.n
    turbines = sorted(((x, u) for u, x in enumerate(crp.turbines[: -1])), key=lambda val: atan2(val[0][1], val[0][0]))
    for x, u in turbines:
      if used + 1 > crp.cable_capacity[-1]:
        tree[v] = crp.n
        used = 0
      elif v != -1:
        tree[v] = u
      v = u
      used += 1

    assert v != -1, "Unexpected end node"
    tree[v] = crp.n

    return tree
