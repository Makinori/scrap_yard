import numpy as np
import math

import matplotlib.pyplot as plt
from matplotlib.image import imread

# mnist
from dataset.mnist import load_mnist
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)


def show_image_list(image_list, width=False, height=False):
    print("plotting image")
    list_size = len(image_list)

    if not width : width = np.sqrt(len(image_list[0]))
    
    for i in range(list_size):
        
        plt.subplot(math.ceil(np.sqrt(list_size)),  math.ceil(np.sqrt(list_size)),i+1)
        plt.imshow(x_train[i].reshape(28,28), cmap=plt.cm.gray_r, interpolation='nearest')
        plt.xticks([], [])
        plt.yticks([], [])

    plt.show()
    


class Layer:
    def __init__(self):
        pass
    def forwrd(self, x):
        pass
    def backprop(self, df_cross):
        pass


class Relu(Layer):
    def __init__(self):
        self.x = None
        self.y = None
    def forward(self, x):
        self.x = x
        x > 0

    def backprop(self, df_cross):
        pass

class NeuralNet:
    def __init__(self):
        pass



if __name__=="__main__":
    show_image_list(x_train[0:5])
