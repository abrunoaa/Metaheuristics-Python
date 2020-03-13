from combinatorial.cvrp.solution import Solution
from combinatorial.simulated_annealing import simulated_annealing

from run_tests import run


def function(cvrp):
  max_temperature = 2 * cvrp.number_of_clients
  min_temperature = 1
  cooling_rate = .99
  return simulated_annealing(max_temperature, min_temperature, cooling_rate, Solution(cvrp))


# debugging
if __name__ == "__main__":
  run('A\\A-n32-k5.vrp', 100, function)
  # run('X\\X-n256-k16.vrp', 100, function)
