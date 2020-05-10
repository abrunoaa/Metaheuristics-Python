#  instance.py
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
from abc import ABC, abstractmethod


class Instance(ABC):
  """
  This class defines what an instance must have.
  """

  @abstractmethod
  def get_n(self):
    """
    Number of nodes in this instance.

    :return: The number of nodes in this instance
    """
    pass

  @abstractmethod
  def get_locations(self):
    """
    Return the 2D location of all nodes.

    :return: Location of all nodes
    """
    pass

  @abstractmethod
  def cost(self, u: int, v: int):
    """
    Cost to travel from u to v.

    :param u: Node from graph.
    :param v: Node from graph.
    :return: The cost to travel from u to v.
    """
    pass

  @staticmethod
  @abstractmethod
  def read(filename):
    """
    Read a instance from file.

    :param filename: File to read.
    :return: The instance read from file.
    """
    pass
