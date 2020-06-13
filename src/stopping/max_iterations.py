#  max_iterations.py
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


class MaxIterations(StoppingCondition):
  """
  Create a stop criteria with limit of iterations.
  """

  def __init__(self, max_iterations: int):
    """
    :param max_iterations: Maximum number of iterations.
    """
    self.counter = 0
    self.max_iterations = max_iterations

  def start(self) -> None:
    self.counter = 0

  def finished(self):
    return self.counter >= self.max_iterations

  def update(self, improved: bool):
    self.counter += 1

  def timing(self) -> float:
    return self.counter / self.max_iterations
