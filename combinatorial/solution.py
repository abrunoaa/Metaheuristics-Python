#  solution.py
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

from abc import ABC, abstractmethod


class Solution(ABC):

  def __str__(self):
    return str(self.get_fitness()) + " " + str(self.get_tour())

  @abstractmethod
  def get_fitness(self):
    pass

  @abstractmethod
  def get_tour(self):
    pass

  @abstractmethod
  def neighbor(self):
    pass

  @abstractmethod
  def local_search(self):
    pass
