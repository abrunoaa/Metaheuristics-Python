#  metaheuristic.py
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
from abc import ABC, abstractmethod, ABCMeta


class Metaheuristic(ABC):
  """
  Class to define behavior of metaheuristics.
  """

  @staticmethod
  @abstractmethod
  def build(*args):
    """
    Build one instance of current metaheuristic.

    :param args: Arguments of metaheuristic
    :return: New instance of metaheuristic
    """
    pass

  @abstractmethod
  def execute(self, initial_values):
    """
    Execute current metaheuristic with the given initial solution.

    :param initial_values: An initial solution, which must be a single solution
    :return: The best found solution
    """
    pass


# FIXME: Does we really need these separation?
class MetaheuristicSingleSolution(Metaheuristic, metaclass=ABCMeta):
  """
  Class to define behavior of metaheuristics of single solution.
  """
  pass


class MetaheuristicPopulationBased(Metaheuristic, metaclass=ABCMeta):
  """
  Class to define behavior of metaheuristics of population based.
  """
  pass
