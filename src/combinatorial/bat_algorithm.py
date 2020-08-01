#  bat_algorithm.py
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
from random import random
from typing import List

from combinatorial.bat import Bat
from combinatorial.metaheuristic import MetaheuristicPopulationBased
from util.range_util import ensure_range


class BatAlgorithm(MetaheuristicPopulationBased):
    # TODO: add type hint
    # TODO: add docs

    @staticmethod
    def build(pulse_rate, loudness, stop_condition):
        return BatAlgorithm((pulse_rate, loudness, stop_condition))

    def __init__(self, args):
        self.__pulse_rate = args[0]
        self.__loudness = args[1]
        self.__stop_condition = args[-1]

    def execute(self, bats: List[Bat]):
        r = self.__pulse_rate
        a = self.__loudness
        best = deepcopy(min(bats))

        self.__stop_condition.start()
        while not self.__stop_condition:
            for bat in bats:
                bat.update()

            if random() > r:
                bats.sort()
                for bat in bats[: max(1, int(r * len(bats)))]:
                    bat.local_search()

            # FIXME: missing Lévy flight

            tmp = min(bats)
            if random() < a and tmp.get_fitness() < best.get_fitness():
                t = self.__stop_condition.timing()
                r = ensure_range(r + t, 0, .99)
                a = ensure_range(a - t, .01, 1)

            improved = tmp.get_fitness() < best.get_fitness()
            if improved:
                best = deepcopy(tmp)

            self.__stop_condition.update(improved)

        return best
