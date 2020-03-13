from math import exp
from random import uniform
from logging import info

from combinatorial.solution import Solution


def simulated_annealing(initial_temperature, min_temperature, alpha, initial_solution: Solution):
  """
  Simulated Annealing implementation. This function works based on class Solution.
  :param initial_temperature: The initial temperature of algorithm.
  :param min_temperature: The stopping temperature of algorithm.
  :param alpha: The factor of cooling.
  :param initial_solution: A starting solution, which is expected to be based on class Solution.
  :return: The best found solution.
  """
  info("Starting simulated annealing")
  best = initial_solution
  x = best
  temperature = initial_temperature
  while temperature > min_temperature:
    info("SA searching for new solution")
    y = x.neighbor()
    y.local_search()
    if y.get_fitness() < x.get_fitness() or uniform(0, 1) < exp((x.get_fitness() - y.get_fitness()) / temperature):
      x = y
      if x.get_fitness() < best.get_fitness():
        best = x
    temperature *= alpha
  return best
