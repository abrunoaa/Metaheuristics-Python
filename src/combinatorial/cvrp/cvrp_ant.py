#  cvrp_ant.py
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
from random import sample

from combinatorial.ant import Ant
from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_solution import CvrpSolution
from util.random_util import roulette


class CvrpAnt(Ant, CvrpSolution):

    def __init__(self, cvrp: Cvrp, tour = None):
        super().__init__(cvrp, tour)
        self.neighbor = []
        self.lower = 0

    def set_neighbors(self, values, lower):
        self.neighbor = values
        self.lower = lower

    def update_delta(self, delta) -> None:
        change = 1 / self.fitness
        for i, j in self._truck_ranges():
            u = 0
            for v in self.tour[i: j + 1]:
                delta[u][v] += change
                u = v
            delta[u][0] += change

    # FIXME:
    #   Why the solution is better for higher values of alpha and beta?
    #   Because the variables are small and becomes 0?
    def travel(self, alpha, beta, pheromone, quality):
        n = len(pheromone) - 1
        self.tour.clear()

        u = 0
        load = 0
        candidate = set(range(n + 1))
        while len(candidate) > 1:
            if len(candidate) <= self.lower:
                u_candidates = list(candidate)
            else:
                u_candidates = [v for v in self.neighbor[u] if v in candidate]
                if len(u_candidates) < self.lower:
                    u_candidates += sample(list(candidate), self.lower - len(u_candidates))

            probability = [pheromone[u][v] ** alpha * quality[u][v] ** beta for v in u_candidates]
            u = u_candidates[roulette(x for x in probability)]
            if u == 0 or load + self.cvrp.get_demand(u) > self.cvrp.capacity:
                u = 0
                load = 0
            else:
                load += self.cvrp.get_demand(u)
                candidate.remove(u)
                self.tour.append(u)

        self._find_fitness_and_optimal_trucks()
