#  simulated_annealing_cvrp.py
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

from combinatorial.cvrp.solution import Solution
from combinatorial.simulated_annealing import simulated_annealing

from combinatorial.run_tests import run


def function(cvrp):
  max_temperature = 10
  min_temperature = 1
  cooling_rate = .999
  return simulated_annealing(max_temperature, min_temperature, cooling_rate, Solution(cvrp))


# debugging
if __name__ == "__main__":
  run('A\\A-n32-k5.vrp', 100, function)
  # run('X\\X-n256-k16.vrp', 100, function)
