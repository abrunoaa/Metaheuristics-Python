#  max_no_improve.py
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


class MaxNoImprove(StoppingCondition):
  """
  Stop criteria limited by the number of iterations without improvement.
  """

  def __init__(self, max_no_improve: int):
    """
    :param max_no_improve: Maximum of iterations without improving.
    """
    if max_no_improve < 1:
      raise ValueError("Invalid iteration limit: {} < 1".format(max_no_improve))

    self.counter = None
    self.phi = None
    self.max_no_improve = max_no_improve

  def start(self) -> None:
    self.counter = 0
    self.phi = 0

  def finished(self):
    return self.counter >= self.max_no_improve

  def update(self, improved: bool):
    if improved:
      self.counter = 0
    else:
      self.counter += 1

  def timing(self) -> float:
    phi = self.phi * max(0.0, 1.0 - 10.0 / self.max_no_improve)
    self.phi = phi + (1 - phi) * (self.counter / self.max_no_improve)
    # self.phi = self.counter / self.max_no_improve
    return self.phi
