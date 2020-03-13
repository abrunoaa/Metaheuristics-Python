from bisect import bisect_left
from itertools import accumulate
from random import uniform, random


def genetic_algorithm(iterations, crossover, elitism, mutation, population):
  assert 0 <= crossover <= 1
  assert 0 <= elitism <= 1
  assert 0 <= mutation <= 1
  assert len(population) >= 2
  assert int(len(population) * elitism) < len(population)

  pop_len = len(population)
  population = sorted(population, key=lambda x: x.get_fitness())
  best = population[0]
  elitism = int(elitism * len(population))
  for i in range(iterations):
    high = population[-1].get_fitness()
    probability = list(accumulate(high - population[i].get_fitness() + 1 for i in range(len(population))))
    for j in range(elitism, pop_len):
      if random() < crossover:
        k = bisect_left(probability, uniform(0, probability[-1]))
        assert k != len(probability), "Impossible selection occurred!"
        if k == j:
          k -= 1
        population[j].mate(population[k])
      if random() < mutation:
        population[j].mutate()
      population[j].two_opt()
    population = sorted(population, key=lambda x: x.get_fitness())

  return best
