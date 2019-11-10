import sys
import os

import numpy as np

sys.path.insert(0, '../evoman_framework/evoman')

from environment import Environment
from controller import Controller

from network import NeuroEvolution

# numpy.random.choice([1,0])
class CustomController(Controller):

    def control(self, params, cont = None):

        print(type(params))
        print(params)

        if sum(abs(params)) > 100:
            action1 = 0
            action2 = 1
            action3 = 1
            action4 = 1
            action5 = 0
        else:
            action1 = 1
            action2 = 0
            action3 = 1
            action4 = 1
            action5 = 0

        return [action1, action2, action3, action4, action5]


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