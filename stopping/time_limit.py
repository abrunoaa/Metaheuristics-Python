#  time_limit.py
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
from time import time
from typing import Union

from stopping.stopping_criteria import StoppingCriteria


class TimeLimit(StoppingCriteria):
  """
  Stop criteria with limit of executing time.
  """

  def __init__(self, max_seconds: Union[int, float]):
    """
    Create a stop criteria with time limit.

    Time starts counting immediately.

    :param max_seconds: Maximum number of seconds of execution.
    """
    self.start_time = time()
    self.max_seconds = max_seconds

  def finished(self):
    return (time() - self.start_time) >= self.max_seconds

  def update(self, improved: bool):
    pass
