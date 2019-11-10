import sys
import os

import numpy as np

sys.path.insert(0, 'evoman')

from environment import Environment
from controller import Controller

from network import NeuroEvolution

experiment_name = 'test'

if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)

custom_controller = NeuroEvolution()
env = Environment(speed="normal",
                  enemymode="static",
                  player_controller=custom_controller)

if __name__=='__main__':
    env.update_parameter('contacthurt','player')
    f, p, e, t = env.play()