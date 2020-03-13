from combinatorial.cvrp.cvrp import Cvrp

from time import process_time as time


# import logging
# logging.getLogger().setLevel(logging.DEBUG)

def run(filename, tests, function):
  cvrp = Cvrp.read(filename)
  total_elapsed = 0
  avg_answer = 0
  best, worst = float("inf"), 0
  print("elapsed,result,tour")

  for test in range(tests):
    start = time()
    ans = function(cvrp)
    end = time()

    elapsed = end - start
    print("{:.3f}s,{},{}".format(elapsed, ans.get_fitness(), ans.get_tour()))

    total_elapsed += elapsed
    avg_answer += ans.get_fitness()
    best = min(best, ans.get_fitness())
    worst = max(worst, ans.get_fitness())

  print("avg_elapsed,avg_result,best_result,worst_result")
  print("{:.3f}s,{:.3f},{},{}".format(total_elapsed / tests, avg_answer / tests, best, worst))
