#  cvrp_bat.py
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
from random import random, randrange
from typing import List

from combinatorial.bat import Bat
from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_solution import CvrpSolution
from util.range_util import ensure_range


# TODO: validate arguments
# TODO: document this file
class CvrpBat(Bat, CvrpSolution):

    def __init__(self, cvrp: Cvrp, tour: List[int] = None):
        f = 1 - 10 / cvrp.n
        self.frequency = f + (1 - f) * random()
        super().__init__(cvrp, tour)

    def update(self):
        i = randrange(0, self.cvrp.get_n() - 1)
        j = randrange(i + 2, self.cvrp.get_n() + 1)
        new_tour = self.tour[:i] + self.tour[i: j][::-1] + self.tour[j:]

        self.frequency = ensure_range(self.frequency * .95, .1, 1)
        for k in range(int(self.frequency * self.cvrp.n)):
            i = randrange(self.cvrp.n)
            j = randrange(self.cvrp.n)
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        self.tour = new_tour
        self._find_fitness_and_optimal_trucks()
