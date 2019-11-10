import sys
import os

import numpy as np

from keras.models import load_model
sys.path.insert(0, 'evoman')

from environment import Environment
from controller import Controller

experiment_name = 'test'

if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)

if __name__=='__main__':
    # Defining controller
    example = load_model('models/test.pkl')

    env = Environment(speed="normal",
                      enemymode="static",
                      player_controller=example,
                      enemies=[1, 3, 5, 8],
                      multiplemode="yes",
                      level=2)

    env.update_parameter('contacthurt', 'player')

    f, p, e, t = env.play()
    print(f)