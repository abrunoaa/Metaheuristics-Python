#  lin_kernighan.py
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
from typing import Callable, List

from util.list_util import rotate


def __travel(n: int, t: List[int], apply: Callable):
  assert len(t) >= 4
  assert len(t) % 2 == 0
  assert len(set(t)) == len(t), "Duplicates found in changes"
  assert all(0 <= x < n for x in t)

  m = len(t)
  neighbor = [[(u - 1) % n, (u + 1) % n] for u in range(n)]
  for k in range(m):
    tp = +1 if k % 2 == 0 else -1
    tmp = neighbor[t[k]]
    assert t[(k + tp) % len(t)] in tmp
    tmp[0 if tmp[0] == t[(k + tp) % m] else 1] = t[(k - tp) % m]
    if tmp[0] == tmp[1]:
      raise ValueError("Invalid tour")

  vis = [False for _ in range(n)]
  w = t[0]
  prev_node = neighbor[w][0]
  while not vis[w]:
    vis[w] = True
    apply(w)
    next_node = next(x for x in neighbor[w] if x != prev_node)
    assert prev_node in neighbor[w]
    assert next_node in neighbor[w]
    prev_node, w = w, next_node

  if not all(vis):
    raise ValueError("Invalid tour")


def __creates_cycle(n: int, t: List[int]):
  try:
    __travel(n, t, lambda x: None)
  except ValueError:
    return True
  return False


def __best_move(t: List[int], tour: List[int], cost: Callable):
  """
  Returns the nodes to add to list t which has the best saving cost.

  :param t: Position of nodes to exchange (on tour)
  :param tour: The tour
  :param cost: Function that returns the cost between two nodes
  :return: A tuple with the best cost, first node and second node
  """
  n = len(tour)
  assert len(t) >= 2
  assert all(0 <= x < n for x in t)

  a = t[-1]
  b = t[0]
  tmp = t + [-1, -1]
  best_improve = 0, -1, -1
  for v in range(n):
    if v in t:
      continue

    u = (v - 1) % n
    if u in t:
      continue

    tmp[-2] = u
    tmp[-1] = v
    if __creates_cycle(n, tmp):
      u, v = v, u

      tmp[-2] = u
      tmp[-1] = v
      assert not __creates_cycle(n, tmp), "Must remove the cycle"

    assert 0 <= u < n
    assert 0 <= v < n
    improve = cost(tour[a], tour[b]) + cost(tour[u], tour[v]) - cost(tour[a], tour[u]) - cost(tour[v], tour[b])
    if improve > best_improve[0]:
      best_improve = improve, u, v

  return best_improve


def __select_moves(tour: List[int], cost: Callable):
  n = len(tour)
  best_improve = 0, []
  for v in range(n):
    u = (v - 1) % n
    improve = 0

    t = [u, v]
    w = __best_move(t, tour, cost)
    while w[0]:
      improve += w[0]
      t += [w[1], w[2]]
      w = __best_move(t, tour, cost)

    if improve > best_improve[0]:
      best_improve = improve, t

  assert best_improve[0] >= 0
  assert best_improve[0] == 0 or len(best_improve[1]) >= 4
  assert len(set(best_improve[1])) == len(best_improve[1])
  return best_improve


def __do_moves(t: List[int], tour: List[int]):
  assert len(t) >= 4
  assert len(set(t)) == len(t), "Duplicates found in changes"
  assert all(0 <= x < len(tour) for x in t)

  n = len(tour)
  new_tour = []
  __travel(n, t, lambda x: new_tour.append(tour[x]))

  assert set(new_tour) == set(tour), "Wrong nodes in new tour"
  tour[:] = new_tour[:]


def lin_kernighan(tour: List[int], cost: Callable):
  improve = 0
  move = __select_moves(tour, cost)
  while move[0]:
    improve += move[0]
    __do_moves(move[1], tour)
    move = __select_moves(tour, cost)

  if tour[-1] != 0:
    rotate(tour, tour.index(0) + 1)
  return improve
