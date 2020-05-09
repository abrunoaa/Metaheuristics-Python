#  run_tests.py
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

from time import process_time as time


def run(instance, solution_builder, number_of_tests, metaheuristic, bks=None):
  """
  Run several tests on an instance with a specific metaheuristic.
  :param instance: Instance to test.
  :param solution_builder: Creates a new solution. This must be callable and receive the instance as argument.
  :param number_of_tests: Number of times to repeat the test.
  :param metaheuristic: Metaheuristic to execute.
  :param bks: Best known solution. If it's present, then the results are checked to see if a new optimum is found.
  :return: None
  """
  total_elapsed = 0
  avg_answer = 0
  best, worst = float("inf"), 0
  print("elapsed;result;tour")

  for test in range(number_of_tests):
    start = time()
    ans = metaheuristic.execute(solution_builder(instance))
    end = time()
    elapsed = end - start

    if isinstance(ans, list):
      ans = ans[0]

    if bks is not None and ans.get_fitness() < bks:
      print("Better optimum found: ", end='')
    print("{:.3f}s;{};{}".format(elapsed, ans.get_fitness(), ans.get_solution()))

    total_elapsed += elapsed
    avg_answer += ans.get_fitness()
    best = min(best, ans.get_fitness())
    worst = max(worst, ans.get_fitness())

  print("")
  print("avg_elapsed;avg_result;best_result;worst_result")
  print("{:.3f}s;{:.3f};{};{}".format(total_elapsed / number_of_tests, avg_answer / number_of_tests, best, worst))
