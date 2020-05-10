#  roulette.py
#
#  Copyright (c) 2020 Bruno Almeda de Oliveira <abrunoaa@gmail.com>
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

from collections import Generator
from random import uniform


def roulette(values):
  """
  Select one index from values.

  The probability to choose index k is 1 / values[k].

  :param values: List with probabilities to choose index k
  :return: An integer in range [0, len(values)), the chosen index
  """
  if isinstance(values, Generator):
    values = list(values)
  r = uniform(0, sum(values))
  s = 0
  for i, x in enumerate(values):
    s += x
    if s > r:
      return i
  return len(values) - 1
