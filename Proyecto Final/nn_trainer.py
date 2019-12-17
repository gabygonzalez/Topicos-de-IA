import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.neural_network import MLPClassifier
from postura import Momentos


def trainning(momento, frames, ys):
    nn = MLPClassifier(hidden_layer_sizes=(10,6), max_iter=10, alpha=1e-5,
                    solver='sgd', verbose=10, random_state=1,
                    learning_rate_init=.03)

    x_train = np.array(momento.hu)
    #print(x_train)
    y_train = np.array(momento.y).flatten()
    #print(y_train)
    x_test = np.array(frames)
    #print(x_test)
    y_test = np.array(ys).flatten()
    #print(y_test)

    scaler = StandardScaler()

    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    nn.fit(x_train, y_train)

    predict_y = nn.predict(x_test)

    print(confusion_matrix(y_test, predict_y))
    print(classification_report(y_test, predict_y))

    #print("train score: %f" % nn.score(x_train, y_train))
    print("test score: %f" % nn.score(x_test, y_test))
    print("test predict: ", nn.predict(x_test))

    return np.array(nn.coefs_[0]).flatten(), np.array(nn.coefs_[1]).flatten()
