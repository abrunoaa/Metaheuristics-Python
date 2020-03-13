from abc import abstractmethod

from combinatorial.solution import Solution


class Chromosome(Solution):
  @abstractmethod
  def mate(self, other):
    pass

  @abstractmethod
  def mutate(self):
    pass
