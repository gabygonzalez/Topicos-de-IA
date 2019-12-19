import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
from sklearn.neural_network import MLPClassifier
from postura import Momentos


def trainning(momento, frames, ys):
    nn = MLPClassifier(hidden_layer_sizes=(20,10,15), max_iter=10, alpha=1e-5,
                    solver='lbfgs', verbose=10, random_state=1,
                    learning_rate_init=.1, activation='identity')

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

    x_train_sc = scaler.transform(x_train)
    x_test_sc = scaler.transform(x_test)

    nn.fit(x_train_sc, y_train)

    predict_y = nn.predict(x_test_sc)

    print(confusion_matrix(y_test, predict_y))
    print(classification_report(y_test, predict_y))
    print(accuracy_score(y_test, predict_y))

    #print("train score: %f" % nn.score(x_train, y_train))
    #print("test score: %f" % nn.score(x_test_sc, y_test))
    #print("test predict: ", nn.predict(x_test_sc))

    return nn.score(x_test_sc, y_test)*100, nn.predict(x_test_sc)

