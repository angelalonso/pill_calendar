#/usr/bin/env python3                                                                                                                                                           
"""
Given an array with test data, we will:
    - Train
    - Predicts given a line of test data

"""

# requires keras and tensorflow
from keras.models import Sequential
from keras.layers import Dense
import numpy

def model(dataset):
    Xdata = [row[1:] for row in dataset]
    Ydata = [row[0] for row in dataset]

    X = numpy.asarray(Xdata)
    Y = numpy.asarray(Ydata)

    # create model
    print(str(dataset[100]))
    print(str(X[100]))
    print(str(Y[100]))
    model = Sequential()
    model.add(Dense(12, input_dim=11, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    ## Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    ## Fit the model
    model.fit(X, Y, epochs=150, batch_size=10)
    ## evaluate the model
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
