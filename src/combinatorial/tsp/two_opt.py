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
from math import sqrt
from typing import Callable, List

from util.list_util import reverse, rotate

n = 0
s = 0
dis = []


def __best_two_opt_move(tour: List[int], distance: Callable):
    best = (0, [])
    for i in range(0, n - 2):
        a, b = tour[i - 1], tour[i]
        for j in range(i + 2, min(n, i + s + 2)):
            c, d = tour[j - 1], tour[j]
            cur = dis[i] + dis[j] - distance(a, c) - distance(b, d)
            if cur > best[0]:
                best = cur, [(i, j)]

    return best


# noinspection DuplicatedCode
def __run(opt: Callable, tour: List[int], distance: Callable):
    assert 0 in tour, "Expected depot in the tour"
    assert len(set(tour)) == len(tour), "Duplicated node"

    global n, s, dis

    n = len(tour)
    s = int(sqrt(n)) + 1
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
