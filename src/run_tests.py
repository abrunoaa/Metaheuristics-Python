#  run_tests.py
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
from copy import deepcopy
from time import process_time as time
from typing import Callable

from combinatorial.instance import Instance
from combinatorial.metaheuristic import Metaheuristic


def run(instance: Instance, metaheuristic: Metaheuristic, solution_builder: Callable, number_of_tests: int):
  """
  Run several tests on an instance with a specific metaheuristic.

  :param instance: Instance to test.
  :param metaheuristic: Metaheuristic to execute.
  :param solution_builder: Creates a new solution. This must be callable and receive the instance as argument.
  :param number_of_tests: Number of times to repeat the test.
  :return: A tuple with the results with the time they spent.
  """
  if number_of_tests < 1:
    raise ValueError("Invalid number of tests: {}".format(number_of_tests))

  for mh in (deepcopy(metaheuristic) for _ in range(number_of_tests)):
    start = time()
    ans = mh.execute(solution_builder(instance))
    end = time()
    elapsed = end - start
    yield ans, elapsed


def run_and_print(instance: Instance,
                  metaheuristic: Metaheuristic,
                  solution_builder: Callable,
                  number_of_tests: int):
  avg_answer = 0
  avg_time = 0
  best, worst = float("inf"), float("-inf")

  print('elapsed;fitness;solution')
  for ans, elapsed in run(instance, metaheuristic, solution_builder, number_of_tests):
    print('{:.2f}s;{};{}'.format(elapsed, ans.get_fitness(), ans.get_solution()), flush=True)

    best = min(best, ans.get_fitness())
    worst = max(worst, ans.get_fitness())
    avg_answer += ans.get_fitness()
    avg_time += elapsed
  avg_time /= number_of_tests
  avg_answer /= number_of_tests

  print('')
  print('avg_time;avg_ans;best;worst')
  print('{:.2f}s;{:.2f};{};{}'.format(avg_time, avg_answer, best, worst), flush=True)
