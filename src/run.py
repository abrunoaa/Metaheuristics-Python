#  run.py
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
import sys
from argparse import ArgumentParser, FileType, ArgumentTypeError
from copy import deepcopy
from time import process_time as time
from typing import Callable

from combinatorial.ant_colony import AntColonyOptimization
from combinatorial.bat_algorithm import BatAlgorithm
from combinatorial.crp.crp import Crp
from combinatorial.crp.crp_neighborhood import CrpNeighborhood
from combinatorial.crp.crp_solution import CrpSolution
from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_ant import CvrpAnt
from combinatorial.cvrp.cvrp_bat import CvrpBat
from combinatorial.cvrp.cvrp_chromosome import CvrpChromosome
from combinatorial.cvrp.cvrp_particle import CvrpParticle
from combinatorial.cvrp.cvrp_solution import CvrpSolution
from combinatorial.genetic_algorithm import GeneticAlgorithm
from combinatorial.instance import Instance
from combinatorial.metaheuristic import Metaheuristic
from combinatorial.particle_swarm import ParticleSwarm, plt
from combinatorial.simulated_annealing import SimulatedAnnealing
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.tsp_ant import TspAnt
from combinatorial.tsp.tsp_chromosome import TspChromosome
from combinatorial.tsp.tsp_solution import TspSolution
from combinatorial.variable_neighborhood import VariableNeighborhoodSearch
from stopping.max_iterations import MaxIterations
from stopping.max_no_improve import MaxNoImprove
from stopping.no_stop import NoStop
from stopping.time_limit import TimeLimit

DEFAULT_REPEAT = 1
DEFAULT_POP_SIZE = 25

INSTANCE_TYPES = {'CRP': Crp, 'CVRP': Cvrp, 'TSP': Tsp}

SINGLE_SOLUTION = {'SA', 'VNS'}

ARGS_BUILDER = {
  ('ACO', 'CRP'): None, ('ACO', 'CVRP'): CvrpAnt, ('ACO', 'TSP'): TspAnt,
  ('BA', 'CRP'): None, ('BA', 'CVRP'): CvrpBat, ('BA', 'TSP'): None,
  ('GA', 'CRP'): None, ('GA', 'CVRP'): CvrpChromosome, ('GA', 'TSP'): TspChromosome,
  ('PSO', 'CRP'): None, ('PSO', 'CVRP'): CvrpParticle, ('PSO', 'TSP'): None,
  ('SA', 'CRP'): CrpSolution, ('SA', 'CVRP'): CvrpSolution, ('SA', 'TSP'): TspSolution,
  ('VNS', 'CRP'): CrpNeighborhood, ('VNS', 'CVRP'): None, ('VNS', 'TSP'): None,
}


def extract_parameters(params):
  parameters = {}
  for var in params.split(','):
    p = var.split('=')
    if len(p) != 2:
      raise ArgumentTypeError("expected exactly two values per variable: {}".format(var))
    try:
      exec('{} = {}'.format(p[0], float(p[1])), {}, parameters)
    except ValueError:
      raise ArgumentTypeError("invalid number: {}".format(var))
    except SyntaxError:
      raise ArgumentTypeError("invalid variable: {}".format(var))

  return parameters


def read_instance(io, problem):
  return INSTANCE_TYPES[problem].read(io)


def build_algorithm(algorithm, n):
  if algorithm == 'ACO':
    pheromone = AntColonyOptimization.default_pheromone(n)
    return AntColonyOptimization.build(pheromone, alpha=1, beta=10, rho=0.5, stopping_condition=MaxNoImprove(200))

  if algorithm == 'BA':
    return BatAlgorithm.build(pulse_rate = .01, loudness = .99, stop_condition = MaxNoImprove(10 * n))

  if algorithm == 'GA':
    return GeneticAlgorithm.build(crossover=.9, elitism=.9, mutation=.9, stopping_condition=MaxNoImprove(500))

  if algorithm == 'SA':
    return SimulatedAnnealing.build(start_temperature = 1000, min_temperature = 1, alpha = .999, stop_condition = NoStop())

  if algorithm == 'PSO':
    return ParticleSwarm.build(w=.5, c1=.2, c2=.3, stopping_condition=MaxNoImprove(n))

  if algorithm == 'VNS':
    return VariableNeighborhoodSearch.build(stopping_condition = MaxNoImprove(1000))

  raise ArgumentTypeError("invalid algorithm: {}".format(algorithm))


def build_solution_builder(algorithm: str, problem: str, pop_size: int):
  if ARGS_BUILDER[algorithm, problem] is None:
    raise NotImplementedError("{} wasn't implemented with {}".format(problem, algorithm))

  if algorithm in SINGLE_SOLUTION:
    return ARGS_BUILDER[algorithm, problem]

  if algorithm == 'PSO' and problem == 'CVRP':
    return lambda inst: [CvrpParticle(inst, CvrpParticle.grasp(inst, .1)) for _ in range(pop_size)]

  return lambda inst: [ARGS_BUILDER[algorithm, problem](inst) for _ in range(pop_size)]


def parse_args():
  parser = ArgumentParser()
  parser.add_argument("problem", type=str.upper, help="problem to solve", choices=INSTANCE_TYPES.keys())

  algorithms = set(x[0] for x in ARGS_BUILDER.keys())
  parser.add_argument("algorithm", type=str.upper, help="algorithm to use", choices=algorithms)

  # FIXME: the parameters for the algorithm are ignored
  parser.add_argument("-p", "--params", type=extract_parameters, help="parameters for the algorithm (ignored!)")
  parser.add_argument("-s", "--size", type=int, default=DEFAULT_POP_SIZE, help="population size")

  parser.add_argument("-i", "--input", type=FileType('r'), default=sys.stdin, help="file to read instance")
  parser.add_argument("-o", "--output", type=FileType('w'), default=sys.stdout, help="file to write results")

  parser.add_argument("-r", "--repeat", type=int, default=DEFAULT_REPEAT, help="number of times to execute")

  args = parser.parse_args()

  instance = read_instance(args.input, args.problem)
  n = instance.get_n() + 1 if args.problem == 'CVRP' else instance.get_n()

  mh = build_algorithm(args.algorithm, n)
  solution_builder = build_solution_builder(args.algorithm, args.problem, args.size)

  return instance, mh, solution_builder, args.repeat, args.output


def run(instance: Instance, metaheuristic: Metaheuristic, solution_builder: Callable, number_of_tests: int):
  """
  Run several tests on an instance with a specific metaheuristic.

  :param instance: Instance to test.
  :param metaheuristic: Metaheuristic to execute.
  :param solution_builder: Creates a new solution. This must be callable and receive the instance as argument.
  :param number_of_tests: Number of times to repeat the test.
  :return: A tuple with the results with the time they spent.
  """
  if number_of_tests < 1:
    raise ValueError("Invalid number of tests: {}".format(number_of_tests))

  it = 0
  for mh in (deepcopy(metaheuristic) for _ in range(number_of_tests)):
    plt.clear()
    start = time()
    ans = mh.execute(solution_builder(instance))
    end = time()

    # with open('plot-{}.py'.format(it), 'w') as f:
    #   f.write('import sys\n')
    #   f.write('import matplotlib.pyplot as plt\n')
    #   f.write('plt.plot({})\n'.format(plt))
    #   f.write('plt.savefig(sys.stdout.buffer)\n')

    it += 1
    elapsed = end - start
    yield ans, elapsed


def run_and_print(instance, metaheuristic, solution_builder, number_of_tests, output):
  tests_run = 0
  avg_time = 0
  avg_ans, best_ans, worst_ans = 0, float("inf"), float("-inf")
  avg_gap, best_gap, worst_gap = 0, float("inf"), float("-inf")

  bks = instance.get_best()
  if bks is None:
    bks = float("inf")

  try:
    output.write('elapsed;gap;fitness;solution\n')
    for ans, elapsed in run(instance, metaheuristic, solution_builder, number_of_tests):
      fitness = ans.get_fitness() if isinstance(ans.get_fitness(), int) else round(ans.get_fitness(), 2)
      gap = 100 * (fitness - bks) / bks

      output.write('{:.2f}s;{:.6}%;{};{}\n'.format(elapsed, gap, fitness, ans.get_solution()))
      output.flush()

      best_ans = min(best_ans, ans.get_fitness())
      worst_ans = max(worst_ans, ans.get_fitness())
      avg_ans += ans.get_fitness()

      best_gap = min(best_gap, gap)
      worst_gap = max(worst_gap, gap)
      avg_gap += gap

      avg_time += elapsed
      tests_run += 1
  except KeyboardInterrupt:
    pass

  if tests_run:
    avg_time /= tests_run
    avg_ans /= tests_run
    avg_gap /= tests_run

    if not isinstance(best_ans, int):
      best_ans = round(best_ans, 2)
      worst_ans = round(worst_ans, 2)

    output.write('\n')
    if instance.get_best() and best_ans < instance.get_best():
      output.write('NEW OPTIMUM: {}'.format(best_ans))

    output.write('avg_time;avg_ans;best_ans;worst_ans;avg_gap;best_gap;worst_gap\n')
    output.write('{:.2f}s;{:.2f};{};{};{:.6}%;{:.6}%;{:.6}%\n'
                 .format(avg_time, avg_ans, best_ans, worst_ans, avg_gap, best_gap, worst_gap))
    output.flush()

  if output != sys.stdout:
    output.close()


if __name__ == '__main__':
  run_and_print(*parse_args())
