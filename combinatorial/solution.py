#  solution.py
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

from abc import ABC, abstractmethod

from combinatorial.instance import Instance


class Solution(ABC):
  """
  Class to define a solution.
  """

  def __str__(self):
    return str(self.get_fitness()) + " " + str(self.get_solution())

  @abstractmethod
  def get_instance(self) -> Instance:
    """
    :return: The instance of this solution
    """
    pass

  @abstractmethod
  def get_fitness(self):
    """
    :return: Fitness of current solution.
    """
    pass

  @abstractmethod
  def get_solution(self):
    """
    :return: Current tour.
    """
    pass

  @abstractmethod
  def neighbor(self):
    """
    Search for a new solution around current one.

    :return: A new solution based on current one.
    """
    pass

  @abstractmethod
  def local_search(self):
    """
    Move this solution to optimize it.

    :return: None.
    """
    pass

  @abstractmethod
  def validate(self) -> None:
    """
    Abort if current state of solution is invalid.

    Note that validations use assert, which must be enabled, otherwise nothing happens.

    :return: None.
    """
    pass
