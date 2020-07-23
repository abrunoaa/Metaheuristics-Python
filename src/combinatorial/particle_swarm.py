#  particle_swarm.py
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
#
from copy import deepcopy

from combinatorial.metaheuristic import MetaheuristicPopulationBased

plt = []


class ParticleSwarm(MetaheuristicPopulationBased):
  # TODO: add type hint
  # TODO: add docs

  @staticmethod
  def build(w, c1, c2, stopping_condition):
    """
    :param w: Probability to move randomly.
    :param c1: Probability to move towards particle's best.
    :param c2: Probability to move towards global's best.
    :param stopping_condition: Condition to stop the algorithm.
    :return: An instance of Particle Swarm.
    """
    return ParticleSwarm((w, c1, c2, stopping_condition))

  def __init__(self, args):
    self.__w = args[0]
    self.__c1 = args[1]
    self.__c2 = args[2]
    self.__stopping_condition = args[-1]

  def execute(self, particles):
    gbest = min(particles, key=lambda particle: particle.get_fitness())

    # FIXME: currently using dynamic parameters
    # w = self.__w
    # c1 = self.__c1
    # c2 = self.__c2
    self.__stopping_condition.start()
    while not self.__stopping_condition:
      t = self.__stopping_condition.timing()
      # print(self.__stopping_condition.counter, t)
      plt.append(t)
      w = 1 - t
      c1 = .3 * t
      c2 = .5 * t

      improved = False
      for p in particles:
        p.move(gbest, w, c1, c2)
        p.local_search()
        if p.get_fitness() < gbest.get_fitness():
          gbest = deepcopy(p)
          improved = True

      self.__stopping_condition.update(improved)

    return gbest
