#  optimal_split.py
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
from typing import List

from combinatorial.cvrp.cvrp import Cvrp
from util.min_queue import MinQueue


# TODO document this file


def optimal_truck_split(cvrp: Cvrp, tour: List[int]):
  n = cvrp.get_n()
  distances = [cvrp.cost(tour[i], tour[i + 1]) for i in range(n - 1)]

  # cost to return to the depot after i and continue at i + 1
  split = [cvrp.cost(tour[i], 0) + cvrp.cost(0, tour[i + 1]) - distances[i] for i in range(n - 1)] + [-1e9]
  used = 0
  i = 0
  best = None
  path = [None] * n
  queue = MinQueue()
  queue.push((0, -1))
  for j in range(n):
    # move right pointer
    used += cvrp.get_demand(tour[j])

    # move left pointer until the truck load is inside its capacity
    while used > cvrp.get_capacity():
      used -= cvrp.get_demand(tour[i])
      i += 1
      queue.pop()
    assert i <= j

    # store previous truck end point
    best, path[j] = queue.min()
    queue.push((split[j] + best, j))

  # recover the end points
  truck = []
  v = n - 1
  while v != -1:
    truck.append(v)
    v = path[v]
  truck = truck[::-1]

  fitness = best + cvrp.cost(0, tour[0]) + sum(distances) + cvrp.cost(tour[-1], 0)
  return fitness, truck
