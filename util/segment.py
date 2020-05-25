#  segment.py
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


def intersect(a, b, c, d):
  """
  Checks if segment ab intersects with segment cd.

  Each point is represented by a tuple with two values.

  :param a: First point.
  :param b: Second point.
  :param c: Third point.
  :param d: Fourth point.
  :return: True if ab intersect cd. False otherwise.
  """
  def orientation(p, q, r):
    ans = (q[1] - p[1]) * (r[0] - p[0]) - (q[0] - p[0]) * (r[1] - p[1])
    return 0 if ans == 0 else -1 if ans < 0 else 1

  return orientation(a, b, c) * orientation(a, b, d) < 0 \
      and orientation(c, d, a) * orientation(c, d, b) < 0
