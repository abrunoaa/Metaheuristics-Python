#  multiple_condition.py
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

from stopping.stopping_condition import StoppingCondition


class MultipleCondition(StoppingCondition):
  """
  Class to represent multiple criteria.
  """

  def __init__(self, *conditions: StoppingCondition):
    """
    :param conditions: Multiple stopping criteria values to check for.
    """
    self.conditions = conditions

  def start(self) -> None:
    for c in self.conditions:
      c.start()

  def finished(self) -> bool:
    return all(c.finished() for c in self.conditions)

  def update(self, improved: bool) -> None:
    for c in self.conditions:
      c.update(improved)

  def timing(self) -> float:
    return sum(c.timing() for c in self.conditions) / len(self.conditions)
