import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from postura import Momentos

def trainning(momento, frame):
    h = .02  # step size in the mesh

    nn = MLPClassifier(solver='lbfgs', alpha=1.e-05, random_state=1,
                                             hidden_layer_sizes=[30,])

    x_train = np.array(momento.hu)
    #print(x_train)
    y_train = np.array(momento.y).flatten()
    #print(y_train)
    x_test = frame.hu
    #print(x_test)
    y_test = frame.y

    nn.fit(x_train, y_train)

    #print("train: ", nn.score(x_train, y_train))
    #print("test: ", nn.score(x_test, y_test))

    return 0.
