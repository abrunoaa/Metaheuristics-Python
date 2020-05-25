#  stopping_criteria.py
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


class StoppingCriteria(ABC):
  """
  Abstract class to represent a stop criteria and define what it must have.
  """

  def __bool__(self):
    return self.finished()

  @abstractmethod
  def restart(self) -> None:
    """
    Restart this criteria.

    :return: None.
    """
    pass

  @abstractmethod
  def finished(self) -> bool:
    """
    Check if the stopping criteria was reached.

    :return: True if stopping criteria was reached. False otherwise.
    """
    pass

  @abstractmethod
  def update(self, improved: bool) -> None:
    """
    Update the state of current criteria.

    :param improved: True if the solution improved on current iteration. False otherwise.
    :return: None.
    """
    pass
