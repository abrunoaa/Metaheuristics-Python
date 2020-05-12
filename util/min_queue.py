#  min_queue.py
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

from collections import deque


class MinQueue:
  """
  Especial queue that returns the minimum value in it.
  """

  def __init__(self):
    self.data = deque()

  def min(self):
    """
    :return: The minimum value in this queue
    """
    return self.data[0][0]

  def push(self, x):
    """
    Add a value to this queue.

    Due to the queue comparison, it's necessary to implement operator __le__.

    :param x: Value to add to the queue
    :return: None
    """
    k = 1
    while len(self.data) > 0 and x <= self.data[-1][0]:
      k += self.data[-1][1]
      self.data.pop()
    self.data.append([x, k])

  def pop(self):
    """
    Remove the element in the front of the queue.

    Note that the element in the front of the queue doesn't necessarily is the minimum value.

    :return: None
    """
    if self.data[0][1] == 1:
      self.data.popleft()
    else:
      self.data[0][1] -= 1
