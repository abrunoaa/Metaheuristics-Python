#  crp_neighborhood.py
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
from abc import ABCMeta
from random import randrange
from typing import List

from combinatorial.crp.crp import Crp
from combinatorial.crp.crp_solution import CrpSolution
from combinatorial.neighborhood import Neighborhood


class CrpNeighborhood(CrpSolution, Neighborhood, metaclass=ABCMeta):

  def __init__(self, crp: Crp, tree: List[int] = None, fitness: float = None, energy: List[int] = None):
    super().__init__(crp, tree, fitness, energy)

  def shake(self):
    for k in range(self.crp.n):
      candidates = self._get_changing_candidates()
      assert candidates
      p = randrange(len(candidates))
      change = candidates[p]
      self._exchange_inplace(change[1], change[2])
      self.fitness -= change[0]
      self.validate()
