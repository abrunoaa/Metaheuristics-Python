#  multiple_criteria.py
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

from stopping.stopping_criteria import StoppingCriteria


class MultipleCriteria(StoppingCriteria):
  """
  Class to represent multiple criteria.
  """

  def __init__(self, *criteria: StoppingCriteria):
    """
    :param criteria: Multiple stopping criteria values to check for.
    """
    self.criteria = criteria

  def restart(self) -> None:
    for c in self.criteria:
      c.restart()

  def finished(self) -> bool:
    return all(c.finished() for c in self.criteria)

  def update(self, improved: bool) -> None:
    for c in self.criteria:
      c.update(improved)
