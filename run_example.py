import sys
import os

import numpy as np
import pickle

sys.path.insert(0, 'evoman')
sys.path.insert(0, 'agents')


from environment import Environment
from controller import Controller

experiment_name = 'test'

if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)

if __name__=='__main__':
    # Defining controller
    with open('models/pop_100_gen_100__mr_03__1578_simplenet_victor/state_generation_99.pkl', 'rb') as fp:
        population = pickle.load(fp)

    population_ordered = dict(sorted(population.items(), key=lambda x: x[1], reverse=True))

    env = Environment(speed="normal",
                      enemymode="static",
                      player_controller=list(population_ordered.keys())[0],
                      enemies=[1, 2, 3, 4, 5, 6, 7, 8],
                      multiplemode="yes",
                      level=2)

    env.update_parameter('contacthurt', 'player')

    f, p, e, t = env.play()
    print(f)