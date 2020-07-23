#  list_util.py
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
from typing import List


def reverse(lst: List, begin: int = 0, end: int = 1000000000) -> None:
  if begin < 0 <= end:
    for k in range((end - begin) // 2):
      i = begin + k
      j = end - k - 1
      lst[i], lst[j] = lst[j], lst[i]
  else:
    lst[begin: end] = lst[begin: end][::-1]


def rotate(lst: List, new_begin: int, begin: int = 0, end: int = 1000000000) -> None:
  lst[begin: end] = lst[new_begin: end] + lst[begin: new_begin]
