#  cvrp_particle.py
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
from copy import deepcopy
from random import randrange
from typing import List

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_solution import CvrpSolution
from combinatorial.particle import Particle
from util.random_util import roulette


class CvrpParticle(Particle, CvrpSolution):
  # TODO: add docs

  def __init__(self, cvrp: Cvrp, tour: List[int] = None):
    super().__init__(cvrp, tour)
    self.best = deepcopy(self)

  # FIXME: currently works similarly to TSP
  def move(self, gbest: "CvrpParticle", w: float, c1: float, c2: float):
    # extract some range from best and gbest
    best_size = min(int(c1 * self.cvrp.n), self.cvrp.n - 1)
    best_size = 0 if best_size == 0 else randrange(best_size)
    gbest_size = min(int(c2 * self.cvrp.n), self.cvrp.n - 1)
    gbest_size = 0 if gbest_size == 0 else randrange(gbest_size)

    best_start = randrange(self.cvrp.n - best_size)
    gbest_start = randrange(self.cvrp.n - gbest_size)

    gbest_range = gbest.tour[gbest_start: gbest_start + gbest_size]
    gbest_selected = set(gbest_range)
    best_range = [x for x in self.best.tour[best_start: best_start + best_size] if x not in gbest_selected]

    # remaining nodes and random swap
    selected = gbest_selected.union(best_range)
    tour = [x for x in self.tour if x not in selected]
    remaining = len(tour)
    for _ in range(int(w * remaining)):
      i = randrange(remaining)
      j = randrange(remaining)
      tour[i], tour[j] = tour[j], tour[i]

    def add_to_tour(range_to_add):
      if not tour:
        tour[0: 0] = range_to_add
      elif range_to_add:
        cost_to_add = lambda u, v: self.cvrp.cost(u, range_to_add[0]) + self.cvrp.cost(range_to_add[-1], v)
        probability = [cost_to_add(0, tour[0])] + \
                      [cost_to_add(tour[k - 1], tour[k]) for k in range(1, len(tour))] + \
                      [cost_to_add(tour[-1], 0)]

        idx = roulette(probability)
        tour[idx: idx] = range_to_add

    add_to_tour(best_range)
    add_to_tour(gbest_range)

    self.tour = tour
    self._find_fitness_and_optimal_trucks()
