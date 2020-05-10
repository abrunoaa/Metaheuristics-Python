#  tsp_ant.py
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

from typing import List

from combinatorial.ant import Ant
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.tsp_solution import TspSolution
from util.roulette import roulette


class TspAnt(Ant, TspSolution):

  def __init__(self, tsp: Tsp, tour: List[int] = None):
    super().__init__(tsp, tour)

  def travel(self, alpha, beta, pheromone, quality):
    n = len(quality)
    candidate = [u for u in range(1, n)]

    assert len(self.tour) == n
    assert self.tour[-1] == 0

    u = 0
    for i in range(0, n - 1):
      # FIXME:
      #  Why the solution is better for higher values of alpha and beta?
      #  Because they are small and becomes 0?
      probability = [pheromone[u][v] ** alpha * quality[u][v] ** beta for v in candidate]
      u = candidate[roulette(x for x in probability)]
      candidate.remove(u)
      self.tour[i] = u

    self._evaluate_fitness()
    self.validate()
