import sys
import os
import pickle
import logging
import re


import numpy as np

sys.path.insert(0, 'evoman')
sys.path.insert(0, 'agents')


from environment import Environment
from controller import Controller

regex = re.compile(r'(\d+)')

def open_file(filepath, generation):
    with open(os.path.join(filepath, generation), 'rb') as fp:
        population = pickle.load(fp)
    return population

if __name__=='__main__':
    # Defining controller
    trained = [1, 5, 7, 8]
    tested  = [3, 4, 2, 6]

    experiment_name = 'pop_100_gen_100__mr_03__1578_simplenet_victor'

    filepath = os.path.join('models', experiment_name)
    files = os.listdir(filepath)

    generations = {int(regex.findall(file)[0]): file for file in files}
    generations =  sorted(generations.items(), key=lambda x: x[0])
    
    results = dict()

    for generation in generations:
        population = open_file(filepath, generation[1])
        networks = list(population.keys())

        for network in networks:
            
            env = Environment(speed="fastest",
                            enemymode="static",
                            player_controller=network,
                            enemies=tested,
                            multiplemode="yes",
                            level=2,
                            logs='off')

            env.update_parameter('contacthurt', 'player')

            f, p, e, t = env.play()
            results[(generation[0], network)] = [f, p, e, t]
    
    with open(os.path.join(filepath, 'all_results_tested.pkl'), 'wb') as fp:
            pickle.dump(results, fp)