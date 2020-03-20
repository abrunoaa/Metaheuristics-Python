#  simulated_annealing.py
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

from math import exp
from random import uniform
from logging import info

from combinatorial.solution import Solution


def simulated_annealing(initial_temperature, min_temperature, alpha, initial_solution: Solution):
  """
  Simulated Annealing implementation. This function works based on class Solution.
  :param initial_temperature: The initial temperature of algorithm.
  :param min_temperature: The stopping temperature of algorithm.
  :param alpha: The factor of cooling.
  :param initial_solution: A starting solution, which is expected to be based on class Solution.
  :return: The best found solution.
  """
  info("Starting simulated annealing")
  best = initial_solution
  x = best
  temperature = initial_temperature
  while temperature > min_temperature:
    info("SA searching for new solution")
    y = x.neighbor()
    y.local_search()
    if y.get_fitness() < x.get_fitness() or uniform(0, 1) < exp((x.get_fitness() - y.get_fitness()) / temperature):
      x = y
      if x.get_fitness() < best.get_fitness():
        best = x
    temperature *= alpha
  return best
