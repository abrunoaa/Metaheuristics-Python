#  functions.py
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

from math import exp, sqrt, cos, pi, sin

# default dimensions for multidimensional functions
dimensions = 2

# 0
ackley = (dimensions * [(-32, 32)],
          lambda x: -20 * exp(-0.2 * sqrt(1 / len(x) * sum(v ** 2 for v in x)))
                    - exp(1 / len(x) * sum(cos(2 * pi * v) for v in x))
                    + 20 + exp(1))

# -200
ackley2 = (2 * [(-32, 32)], lambda x: -200 * exp(-0.2 * sqrt(x[0] ** 2 + x[1] ** 2)))

# -4.590101633799122
ackley4 = (dimensions * [(-35, 35)],
           lambda x: sum(exp(-0.2) * sqrt(x[i] ** 2 + x[i + 1] ** 2)
                         + 3 * (cos(2 * x[i]) + sin(2 * x[i + 1]))
                         for i in range(len(x) - 1)))

# 0
beale = (2 * [(-4.5, 4.5)],
         lambda x: (1.5 - x[0] + x[0] * x[1]) ** 2
                   + (2.25 - x[0] + x[0] * x[1] ** 2) ** 2
                   + (2.625 - x[0] + x[0] * x[1] ** 3) ** 2)

# -1
easom = (2 * [(-100, 100)], lambda x: -cos(x[0]) * cos(x[1]) * exp(-(x[0] - pi) ** 2 - (x[1] - pi) ** 2))

# 0
rastrigin = (dimensions * [(-5.12, 5.12)], lambda x: 10 * len(x) + sum(v ** 2 - 10 * cos(2 * pi * v) for v in x))

# 0
rosenbrock = (dimensions * [(-5, 10)],
              lambda x: sum(100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2 for i in range(len(x) - 1)))

# 0.292579
schaffer4 = (2 * [(-100, 100)],
             lambda x: 0.5 + (cos(sin(abs(x[0] ** 2 - x[1] ** 2))) ** 2 - 0.5)
                              / (1 + 0.001 * (x[0] ** 2 + x[1] ** 2)) ** 2)
