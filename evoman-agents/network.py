import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation

class NeuroEvolution(object):

    def __init__(self, input_shape=20, output_shape=5):
        self.input_shape = input_shape
        self.output_shape = output_shape

        self._build_model()


    def _build_model(self):

        model = Sequential()
        model.add(Dense(units=4, input_dim=self.input_shape))
        model.add(Activation("relu"))
        model.add(Dense(units=self.output_shape))
        model.add(Activation("softmax"))

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

    def control(self, params, cont=None):
        action1, action2, action3, action4, action5 = self.return_action(params)

        return [action1, action2, action3, action4, action5]

if __name__=='__main__':
    params = np.array([-52.,  -1.,  -1.,  -1.,   0.,   
                        0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,  0.,   0.,   0.,   0.,   0.,   0.])
    
    neural_net = NeuroEvolution()
    print(neural_net.control(params))

