from random import randrange

from combinatorial.chromosome import Chromosome as Base
from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.solution import Solution


class Chromosome(Base, Solution):
  def __init__(self, cvrp: Cvrp, tour = None):
    super().__init__(cvrp, tour)

  def mate(self, other):
    tour1 = self.tour
    tour2 = other.tour
    k = randrange(0, self.cvrp.number_of_clients - 1)
    inserted = set(tour1[: k])
    to_insert = set(v for v in tour2[k:] if v not in inserted)
    self.tour = tour1[: k] + [v for v in tour1[k:] if v not in to_insert] + [v for v in tour2[k:] if v in to_insert]
    self.optimal_split()

  def mutate(self):
    i = randrange(0, self.cvrp.number_of_clients - 1)
    j = randrange(i + 1, self.cvrp.number_of_clients) + 1
    self.tour = self.tour[:i] + self.tour[i: j][::-1] + self.tour[j:]
    self.optimal_split()
