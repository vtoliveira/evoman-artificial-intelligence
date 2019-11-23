import itertools
import os
import pickle

import numpy as np

from network import NeuralNetwork, SimpleNeuralNetwork

class GeneticAlgorithm(object):

    def __init__(self,
                savepath,
                population_size=10,
                number_of_generations=10,
                mutation_rate=0.1,
                load_model=False,
                model=None,
                state=0
                ):
        
        self.savepath = savepath
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.mutation_rate = mutation_rate
        self.load_model = load_model
        self.state = state
        

        if self.load_model==True:
            self.model = model
            with open(os.path.join(self.savepath, self.model), "rb") as fp:
                self.population = pickle.load(fp)
        else:
            self.population = None

    def set_env(self, env):
        self.env = env

    def create_population(self):
        population = dict()
        for i in range(self.population_size):
            # Initialize a neural model
            model = SimpleNeuralNetwork()

            # Calculate fitness
            f, p, e, t = self.fitness(model)
            
            population[model] = f
        
        self.population = population

    def fitness(self, model):
        f, p, e, t = self.env.play(pcont=model)
        print("Fitness: {}\t Player Life: {}\t Enemy Life: {}\n".format(f, p, e))

        return f, p, e, t

    def mutate(self, model):

        # Get model's weights
        weights = model.get_weights()
        n_hidden_layers = len(weights)

        mutate_layer = np.random.choice(n_hidden_layers)
        mutate_value = np.random.uniform(-1, 1)

        if weights[mutate_layer].ndim == 1:
            row_value = np.random.choice(weights[mutate_layer].shape[0])
            weights[mutate_layer][row_value] = mutate_value
        else:
            row_value = np.random.choice(weights[mutate_layer].shape[0])
            col_value = np.random.choice(weights[mutate_layer].shape[1])

            weights[mutate_layer][row_value][col_value] = mutate_value

        model.set_weights(weights)

    def crossover(self, parent, mother):
        # Getting parent and mother weights
        p_weights = parent.get_weights()
        m_weights = mother.get_weights()

        n_hidden_layers = len(p_weights)
        crossover_layer = np.random.choice(n_hidden_layers)

        original_shape = p_weights[crossover_layer].shape
        
        p_stacked_weight = np.hstack(p_weights[crossover_layer])
        m_stacked_weight = np.hstack(m_weights[crossover_layer])

        crossover_point = np.random.choice(p_stacked_weight.shape[0])

        tmp_weight = p_stacked_weight[:crossover_point].copy()
        p_stacked_weight[:crossover_point] = m_stacked_weight[:crossover_point]
        m_stacked_weight[:crossover_point] = tmp_weight

        p_weights[crossover_layer] = p_stacked_weight.reshape(original_shape)
        m_weights[crossover_layer] = m_stacked_weight.reshape(original_shape)

        parent.set_weights(p_weights)
        mother.set_weights(m_weights)

        return parent, mother

    def select_contestant(self, population):
        return np.random.choice(list(population.keys()))

    def single_tournament(self, parent, mother):
        f_p, p, e, t = self.fitness(parent)
        f_m, p, e, t = self.fitness(mother)

        if f_p > f_m:
            return parent, f_p
        else:
            return mother, f_m


    def multiple_tournament(self, parents, offspring):
        new_population = {}

        while len(new_population) != self.population_size:
            contestant_1 = self.select_contestant(parents)
            contestant_2 = self.select_contestant(offspring)

            if parents[contestant_1] > offspring[contestant_2]:
                new_population[contestant_1] = parents[contestant_1]
            else:
                new_population[contestant_2] = offspring[contestant_2]

        return new_population


    def evolve(self):
        if not self.population:
            self.create_population()

        print("Starting Evolution:\n")
        for i in range(self.state, self.number_of_generations):

        
            # Sort population according to fitness value
            print("Best fit for generation: {} is {}".format(i, 
                                    np.max(list(self.population.values()))))

            offspring = {}
            while len(offspring) != self.population_size:

                parents = np.random.choice(list(self.population.keys()), 
                                          size=2,
                                          replace=True)

                new_parent_weight = parents[0].get_weights()
                new_mother_weight = parents[1].get_weights()

                parent = SimpleNeuralNetwork()
                mother = SimpleNeuralNetwork()

                parent.set_weights(new_parent_weight)
                mother.set_weights(new_mother_weight)

                parent, mother = self.crossover(parent, mother)
                children, f_o = self.single_tournament(parent, mother)
                
                offspring[children] = f_o

                # Check for mutation
                if self.mutation_rate > np.random.random():
                    self.mutate(children)
                    print("Mutation happened!\n")

            new_population = self.multiple_tournament(self.population, 
                                                          offspring)

                
            print("Population size: {}".format(len(new_population)))
            self.population = new_population

            self.save_state(i)
        

    def save_state(self, last_generation):
        filename = 'state_generation_' + str(last_generation) + '.pkl'

        with open(os.path.join(self.savepath, filename), 'wb') as fp:
            pickle.dump(self.population, fp)


    def control(self, params, controller):
        params = (params-min(params))/float((max(params)-min(params)))
        action1, action2, action3, action4, action5 = controller.return_action(params)

        return [action1, action2, action3, action4, action5]

