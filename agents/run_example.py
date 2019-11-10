import sys
import os

import numpy as np

sys.path.insert(0, '../evoman_framework/evoman')

from environment import Environment
from controller import Controller

from network import NeuralNetwork
from evolution import GeneticAlgorithm

experiment_name = 'test'

if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)

if __name__=='__main__':
    # Defining controller
    example = NeuralNetwork()
    example.load_model('best_model5.pkl')

    env = Environment(speed="normal",
                      enemymode="static",
                      player_controller=example,
                      enemies=[1, 3, 5, 8],
                      multiplemode="yes",
                      level=2)

    env.update_parameter('contacthurt', 'player')

    f, p, e, t = env.play()
    print(f)