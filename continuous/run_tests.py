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

from time import process_time as time


def run(tests, call, function, interval):
  total_elapsed = 0
  avg_answer = 0
  best, worst = float("inf"), float("-inf")
  print("elapsed;result;tour")

  for test in range(tests):
    start = time()
    ans = call(function, interval)
    end = time()
    elapsed = end - start

    print("{:.3f}s;{:.6f};{}".format(elapsed, ans[0], ["{:.6f}".format(ans[1][i]) for i in range(len(ans[1]))]))

    total_elapsed += elapsed
    avg_answer += ans[0]
    best = min(best, ans[0])
    worst = max(worst, ans[0])

  print("")
  print("avg_elapsed;avg_result;best_result;worst_result")
  print("{:.3f}s;{:.6f};{:.6f};{:.6f}".format(total_elapsed / tests, avg_answer / tests, best, worst))
