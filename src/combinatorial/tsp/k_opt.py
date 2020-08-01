#  k_opt.py
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
from itertools import permutations
from typing import Callable, List, Union

from util.list_util import reverse, rotate

n = 0
dis = []


def __best_two_opt_move(tour: List[int], distance: Callable):
  global n, dis

  best = (0, [])
  for i in range(0, n - 2):
    a, b = tour[i - 1], tour[i]
    for j in range(i + 2, n):
      c, d = tour[j - 1], tour[j]
      cur = dis[i] + dis[j] - distance(a, c) - distance(b, d)
      if cur > best[0]:
        best = cur, [(i, j)]

  return best


def __best_three_opt_move(tour: List[int], distance: Callable):
  def update_best(cost, changes):
    nonlocal best
    if cost > best[0]:
      best = cost, changes

  global n, dis

  best = __best_two_opt_move(tour, distance)
  for i in range(0, n - 4):
    a, b = tour[i - 1], tour[i]
    for j in range(i + 2, n - 2):
      c, d = tour[j - 1], tour[j]
      for k in range(j + 2, n):
        e, f = tour[k - 1], tour[k]
        aux = dis[i] + dis[j] + dis[k]
        update_best(aux - distance(a, c) - distance(b, e) - distance(d, f), [(i, j), (j, k)])
        update_best(aux - distance(a, d) - distance(b, e) - distance(c, f), [(i, j), (j, k), (k - n, i)])
        update_best(aux - distance(a, d) - distance(b, f) - distance(c, e), [(j, k), (k - n, i)])
        update_best(aux - distance(a, e) - distance(b, d) - distance(c, f), [(i, j), (k - n, i)])

  return best


def __run(opt: Callable, tour: List[int], distance: Callable):
  assert 0 in tour, "Expected depot in the tour"
  assert len(set(tour)) == len(tour), "Duplicated node"

  global n, dis

  n = len(tour)
  improve = 0
  initial_cost = sum(distance(tour[i - 1], tour[i]) for i in range(n))

  while True:
    dis = [distance(tour[i - 1], tour[i]) for i in range(n)]
    best = opt(tour, distance)
    if best[0] == 0:
      break

    for change in best[1]:
      reverse(tour, change[0], change[1])
    improve += best[0]

  if tour[-1] != 0:
    rotate(tour, tour.index(0) + 1)

  assert len(set(tour)) == len(tour), "Duplicated node after execution"
  assert initial_cost - improve == sum(distance(tour[i - 1], tour[i]) for i in range(n))
  return improve


def two_opt(tour: List[int], distance: Callable):
  return __run(__best_two_opt_move, tour, distance)


def three_opt(tour: List[int], distance: Callable):
  return __run(__best_three_opt_move, tour, distance)


# FIXME: this function doesn't work for k > 2
def __generic(position: List[int], start: int, k: int, cost: Union[int, float], tour: List[int], distance: Callable):
  if k > 2:
    raise NotImplementedError("Currently doesn't work for k > 2")

  best = (0, [])

  if len(position) < k:
    for j in range(start, n):
      cur = __generic(position + [j], j + 2, k, cost + dis[j], tour, distance)
      if cur[0] > best[0]:
        best = cur
  else:
    assert sum(distance(tour[u - 1], tour[u]) for u in position) == cost, "Invalid cost"
    nodes = [(position[-1] - n, position[0] - 1)]
    nodes += list((position[i - 1], position[i] - 1) for i in range(1, k))
    for r in range(1, 1 << (k - 1)):
      for p in permutations(nodes[: -1]):
        p = list(p) + [nodes[-1]]
        for i in range(k - 1):
          if r & (1 << i):
            p[i] = (p[i][1], p[i][0])

        reduce = cost - sum(distance(tour[p[i - 1][1]], tour[p[i][0]]) for i in range(k))
        if reduce > best[0]:
          best = reduce, p

  return best


def __run_generic(tour: List[int], distance: Callable, k: int):
  assert 0 in tour, "Expected depot in the tour"
  assert len(set(tour)) == len(tour), "Duplicated node"

  global n, dis

  n = len(tour)
  improve = 0

  dis = [distance(tour[i - 1], tour[i]) for i in range(n)]
  best = __generic([], 0, k, 0, tour, distance)
  assert best[0] == __best_three_opt_move(tour, distance)[0]
  while best[0] > 0:
    new_tour = []
    for i, j in best[1]:
      new_tour += [tour[p] for p in range(i, j, (+1 if i < j else -1))] + [tour[j]]

    assert len(new_tour) == n
    tour[0: n] = new_tour[0: n]
    improve += best[0]

    dis = [distance(tour[i - 1], tour[i]) for i in range(n)]
    best = __generic([], 0, k, 0, tour, distance)
    assert best[0] == __best_three_opt_move(tour, distance)[0]

  if tour[-1] != 0:
    depot = tour.index(0) + 1
    rotate(tour, (depot if depot < n else 0))
    dis = [distance(tour[i - 1], tour[i]) for i in range(n)]

  assert k < 2 or __best_two_opt_move(tour, distance)[0] == 0, "Still has optimization"
  assert k < 3 or __best_three_opt_move(tour, distance)[0] == 0, "Still has optimization"

  return improve


def generic(tour: List[int], distance: Callable, k: int):
  return __run_generic(tour, distance, k)
