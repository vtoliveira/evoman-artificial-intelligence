import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation

sigmoid = lambda x: 1 / (1 + np.exp(-x))
relu    = lambda x: np.maximum(x, 0, x)

class NeuralNetwork(object):

    def __init__(self, 
                input_shape=20, 
                n_hidden=10,
                output_shape=5):


        self.input_shape = input_shape
        self._n_hidden = n_hidden
        self.output_shape = output_shape

        self._build_model()

    def _build_model(self):

        model = Sequential()
        model.add(Dense(units=self._n_hidden, input_dim=self.input_shape))
        model.add(Activation("relu"))
        model.add(Dense(units=self.output_shape))
        model.add(Activation("sigmoid"))

        self._model = model

    def return_model(self):
        return self._model

    def return_action(self, inputs):
        inputs = np.array([inputs])
        probabilities = np.round(self._model.predict(inputs))[0]

        left = probabilities[0]
        right = probabilities[1]
        jump = probabilities[2]
        shoot = probabilities[3]
        release = probabilities[4]

        return [left, right, jump, shoot, release]

    def load_model(self, saved_model):
        self._model.load_model(saved_model)

    def control(self, params, cont=None):
        params = (params-min(params))/float((max(params)-min(params)))
        action1, action2, action3, action4, action5 = self.return_action(params)

        return [action1, action2, action3, action4, action5]

class SimpleNeuralNetwork(object):

    def __init__(self, 
                input_shape=20, 
                n_hidden=10,
                output_shape=5):


        self.input_shape = input_shape
        self.n_hidden = n_hidden
        self.output_shape = output_shape

        self.W1 = np.random.uniform(low=-0.5, high=0.5, size=(self.input_shape, n_hidden))
        self.b1 = np.random.uniform(low=-0.5, high=0.5, size=n_hidden)
        self.W2 = np.random.uniform(low=-0.5, high=0.5, size=(self.n_hidden, self.output_shape))
        self.b2 = np.random.uniform(low=-0.5, high=0.5, size=self.output_shape)

        self.weights = [self.W1, self.b1, self.W2, self.b2]

    def predict(self, input):

        y1 = np.dot(input, self.W1) + self.b1
        h1 = relu(y1)
        y2 = np.dot(h1, self.W2) + self.b2
        pred = sigmoid(y2)

        return pred
    
    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights
    
    def return_action(self, inputs):
        # inputs = np.array([inputs])
        probabilities = np.round(self.predict(inputs))

        left = probabilities[0]
        right = probabilities[1]
        jump = probabilities[2]
        shoot = probabilities[3]
        release = probabilities[4]

        return [left, right, jump, shoot, release]

    def control(self, params, cont=None):

        params = (params-min(params))/float((max(params)-min(params)))
        action1, action2, action3, action4, action5 = self.return_action(params)

        return [action1, action2, action3, action4, action5]