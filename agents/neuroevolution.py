import sys
import os

import numpy as np

sys.path.insert(0, 'evoman')

from environment import Environment
from controller import Controller

from evolution import GeneticAlgorithm

experiment_name = 'models/pop_50_gen_40__mr_02__1248_victor'

if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)

if __name__=='__main__':
    ga = GeneticAlgorithm(savepath=experiment_name,
                          population_size=50,
                          number_of_generations=20,
                          mutation_rate=0.2,
                          load_model=False,
                          model='state_generation_9.pkl')

    env = Environment(speed="fastest",
                      enemymode="static",
                      player_controller=ga,
                      enemies=[1, 2, 4, 8],
                      multiplemode="yes",
                      level=2,
                      logs="off")

    env.update_parameter('contacthurt', 'player')

    ga.set_env(env)
    ga.evolve()
    