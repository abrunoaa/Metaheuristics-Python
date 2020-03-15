from combinatorial.cvrp.chromosome import Chromosome
from combinatorial.genetic_algorithm import genetic_algorithm

from combinatorial.run_tests import run


def function(cvrp):
  iterations = 100
  crossover = .9
  elitism = .9
  mutation = .9
  pop_size = 30
  return genetic_algorithm(iterations, crossover, elitism, mutation, [Chromosome(cvrp) for _ in range(pop_size)])


# debugging
if __name__ == "__main__":
  # run('A\\A-n32-k5.vrp', 100, function)
  run('X\\X-n256-k16.vrp', 100, function)
