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

from copy import copy
from logging import info


def two_opt(tour, distance):
  """
  2-opt implementation for routing problems.
  If tour is None or len(tour) < 2, the function will simply return 0 without any errors.
  :param tour: A list-like that represents a tour, which will be modified.
  :param distance: A function which take as argument two nodes and returns a number representing distance.
  :return: A pair with total improvement or 0 if tour is None or len(tour) < 2, and the new tour.
  """
  info("Running 2-opt")

  assert isinstance(tour, list), "'tour' must be a list"
  assert callable(distance), "'distance' must be a function"
  if tour is None or len(tour) < 2:
    return 0, [0]
  assert len(set(tour)) == len(tour), "Duplicates found in tour: {}".format(tour)
  assert tour[-1] == 0, "Expected depot at end of tour, found {}".format(tour[-1])
  tour = copy(tour)
  improve = 0
  n = len(tour)
  while True:
    best = 0
    left = None
    right = None
    dis = [distance(tour[i - 1], tour[i]) for i in range(n)]
    for i in range(-1, n - 3):
      a = tour[i]
      b = tour[i + 1]
      for j in range(i + 2, n - 1):
        c = tour[j]
        d = tour[j + 1]
        reduce = dis[i + 1] + dis[j + 1] - distance(a, c) - distance(b, d)
        if reduce > best:
          best = reduce
          left = i + 1
          right = j
    if best == 0:
      # implementation problems
      assert len(set(tour)) == len(tour) and tour[-1] == 0, "Invalid state after execution"
      return improve, tour
    assert left < right
    improve += best
    tour[left: right + 1] = tour[left: right + 1][::-1]
    assert tour[-1] == 0
    assert len(set(tour)) == n
