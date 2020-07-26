#  two_opt.py
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
from typing import Callable

# from combinatorial.tsp.k_opt import three_opt as tsp_optimizer
from combinatorial.tsp.lin_kernighan import lin_kernighan as tsp_optimizer

exchanges = []

# TODO: Document this file


def __init(n):
  # ensures that row i has i columns for each i in range [0, n)
  while len(exchanges) < n:
    exchanges.append(list(range(len(exchanges))))


def __find_best_optimization(id_i, id_j, tour_i, tour_j, load_i, load_j, demand, cost, capacity):
  best = 0, 0, 0, 0

  used_i = 0
  for i in range(len(tour_i)):
    a, b = tour_i[i - 1], tour_i[i]

    # combine first half with first half
    j = 0
    used_j = 0
    while j < len(tour_j) and (load_i - used_i) + (load_j - used_j) > capacity:
      used_j += demand[tour_j[j]]
      j += 1
    while j < len(tour_j) and used_i + used_j <= capacity:
      c, d = tour_j[j - 1], tour_j[j]
      reduce = cost(a, b) + cost(c, d) - cost(a, c) - cost(d, b)
      if reduce > best[0]:
        best = reduce, i, j, 1

      used_j += demand[tour_j[j]]
      j += 1

    # combine first half with second half
    j = 0
    used_j = 0
    while j < len(tour_j) and used_i + (load_j - used_j) > capacity:
      used_j += demand[tour_j[j]]
      j += 1
    while j < len(tour_j) and (load_i - used_i) + used_j <= capacity:
      c, d = tour_j[j - 1], tour_j[j]
      reduce = cost(a, b) + cost(c, d) - cost(a, d) - cost(c, b)
      if reduce > best[0]:
        best = reduce, i, j, 2

      used_j += demand[tour_j[j]]
      j += 1

    used_i += demand[b]

  return best[0], id_i, id_j, best[1], best[2], best[3]


def __do_exchange(exchange, tour, cost):
  improve, id_i, id_j, i, j, op_type = exchange
  ########################
  # validation
  assert improve > 0
  assert 0 <= id_i < len(tour)
  assert 0 <= id_j < len(tour)
  assert 0 <= i < len(tour[id_i])
  assert 0 <= j < len(tour[id_j])
  assert op_type in [1, 2]

  a = tour[id_i][i - 1]
  b = tour[id_i][i]
  c = tour[id_j][j - 1]
  d = tour[id_j][j]
  assert op_type != 1 or improve == cost(a, b) + cost(c, d) - cost(a, c) - cost(d, b), "invalid improve"
  assert op_type != 2 or improve == cost(a, b) + cost(c, d) - cost(a, d) - cost(c, b), "invalid improve"
  ########################

  # join first route with the second and vice versa
  r1 = tour[id_i]
  r2 = tour[id_j]
  if op_type == 1:
    tour[id_i], tour[id_j] = r1[: i] + r2[: j][::-1] + [0], r1[i: -1][::-1] + r2[j:]
  else:
    tour[id_i], tour[id_j] = r1[: i] + r2[j:], r2[: j] + r1[i:]

  assert tour[id_i][-1] == 0
  assert tour[id_j][-1] == 0
  assert sorted(r1 + r2) == sorted(tour[id_i] + tour[id_j])

  improve += tsp_optimizer(tour[id_i], cost)
  improve += tsp_optimizer(tour[id_j], cost)
  return improve


def two_opt(tour: list, demand: list, capacity: int, cost: Callable):
  """
  Run 2-opt inplace on CVRP tour.

  :param tour: List with routes of CVRP, each one ending with '0'.
  :param demand: Demand of each client.
  :param capacity: Capacity of truck.
  :param cost: Function of two values u and v that calculates the cost for going from u to v.
  :return: Total improvement and new tour.
  """
  global exchanges
  __init(len(tour))

  # optimize each route
  improve = sum(tsp_optimizer(sub_tour, cost) for sub_tour in tour)

  # find the best exchange between every pair of routes
  load = [sum(demand[u] for u in sub) for sub in tour]
  candidates = set()
  for i in range(len(tour)):
    for j in range(i):
      exchanges[i][j] = __find_best_optimization(i, j, tour[i], tour[j], load[i], load[j], demand, cost, capacity)
      if exchanges[i][j][0] > 0:
        candidates.add((exchanges[i][j], i, j))

  # exchange routes to be 2-opt
  while candidates:
    # do the best improvement
    best, i, j = max(candidates)
    improve += __do_exchange(best, tour, cost)
    total = load[i] + load[j]
    load[i] = sum(demand[u] for u in tour[i])
    load[j] = total - load[i]
    assert load[j] == sum(demand[u] for u in tour[j])

    # update the best exchange
    for h in [i, j]:
      for k in range(len(tour)):
        if k != h:
          a, b = (k, h) if k > h else (h, k)
          if exchanges[a][b][0] > 0:
            candidates.remove((exchanges[a][b], a, b))

          exchanges[a][b] = __find_best_optimization(a, b, tour[a], tour[b], load[a], load[b], demand, cost, capacity)
          if exchanges[a][b][0] > 0:
            candidates.add((exchanges[a][b], a, b))

  return improve
