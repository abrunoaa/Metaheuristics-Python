#  two_opt.py
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

from combinatorial.tsp.two_opt import two_opt as tsp_two_opt

from logging import info


def two_opt(tour, truck, demand, capacity, distance):
  """
  Run 2-opt adaptation from TSP to CVRP.
  It's guaranteed that there is no pair which exchange will improve fitness cost.
  :return: None.
  """
  improve = 0

  # split tour to small TSP and optimize
  split_tour = [tour[i: j + 1] + [0] for i, j in zip([0] + [k + 1 for k in truck[:-1]], truck)]
  for i in range(len(split_tour)):
    partial, split_tour[i] = tsp_two_opt(split_tour[i], distance)
    improve += partial

  # exchange routes to be 2-opt
  while True:
    load = [sum(demand[u] for u in st) for st in split_tour]
    ntour = len(split_tour)
    best = 0
    t1 = t2 = p1 = p2 = op_type = None

    # search for best point
    for p in range(ntour):
      used_p = 0
      for i in range(len(split_tour[p])):
        a = split_tour[p][i - 1]
        b = split_tour[p][i]

        for q in range(p + 1, ntour):
          # combine first half with first half
          used_q = 0
          for j in range(len(split_tour[q])):
            if (load[p] - used_p) + (load[q] - used_q) <= capacity:
              c = split_tour[q][j - 1]
              d = split_tour[q][j]
              reduce = distance(a, b) + distance(c, d) - distance(a, c) - distance(d, b)
              if reduce > best:
                best = reduce
                t1, t2 = p, q
                p1, p2 = i, j
                op_type = 1
            used_q += demand[split_tour[q][j]]
            if used_p + used_q > capacity:
              break

          # combine first half with second half
          used_q = 0
          for j in range(len(split_tour[q])):
            if used_p + (load[q] - used_q) <= capacity:
              c = split_tour[q][j - 1]
              d = split_tour[q][j]
              reduce = distance(a, b) + distance(c, d) - distance(a, d) - distance(c, b)
              if reduce > best:
                best = reduce
                t1, t2 = p, q
                p1, p2 = i, j
                op_type = 2
            used_q += demand[split_tour[q][j]]
            if (load[p] - used_p) + used_q > capacity:
              break

        used_p += demand[b]

    if best == 0:
      break
    info("Found optimization of type {}".format(op_type))
    improve += best
    r1 = split_tour[t1]
    r2 = split_tour[t2]
    st = r1 + r2
    if op_type == 1:
      split_tour[t1], split_tour[t2] = r1[: p1] + r2[: p2][::-1] + [0], r1[p1: -1][::-1] + r2[p2:]
    else:
      split_tour[t1], split_tour[t2] = r1[: p1] + r2[p2:], r2[: p2] + r1[p1:]
    assert split_tour[t1][-1] == 0
    assert split_tour[t2][-1] == 0
    assert sorted(st) == sorted(split_tour[t1] + split_tour[t2])

    partial, split_tour[t1] = tsp_two_opt(split_tour[t1], distance)
    improve += partial
    partial, split_tour[t2] = tsp_two_opt(split_tour[t2], distance)
    improve += partial

  tour = []
  truck = []
  for t in split_tour:
    if len(t) != 1:
      tour += t[: -1]
      truck.append(len(tour) - 1)

  return improve, tour, truck
