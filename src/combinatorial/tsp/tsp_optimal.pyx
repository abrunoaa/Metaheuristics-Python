#  tsp.py
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
cdef extern from *:
    """
    #define maxn 10
    """
    cdef const int maxn = 10

cdef int dp[1 << (maxn - 1)][maxn]

cpdef tsp_optimal(tsp):
  """
  Find the optimal solution to TSP.
  
  Note that this only works if the instance has integer costs.
  
  :param tsp: TSP instance to look for best solution 
  :return: The optimal value
  """
  cdef int n = tsp.get_n()
  cdef int tmp

  if n > maxn:
    raise ValueError("Can't process instances with {} nodes; maximum = {}".format(n, maxn))

  for u in range(n):
    dp[0][u] = tsp.cost(u, n - 1)
  for d in range(1, 1 << (n - 1)):
    for u in range(n):
      if not d & (1 << u):
        dp[d][u] = int(1e9)
        for v in range(n - 1):
          if d & (1 << v):
            tmp = dp[d - (1 << v)][v] + tsp.cost(u, v)
            if tmp < dp[d][u]:
              dp[d][u] = tmp

  return dp[(1 << (n - 1)) - 1][n - 1]
