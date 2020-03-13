from abc import ABC, abstractmethod


class Solution(ABC):

  def __str__(self):
    return str(self.get_fitness()) + " " + str(self.get_tour())

  @abstractmethod
  def get_fitness(self):
    pass

  @abstractmethod
  def get_tour(self):
    pass

  @abstractmethod
  def neighbor(self):
    pass

  @abstractmethod
  def local_search(self):
    pass
