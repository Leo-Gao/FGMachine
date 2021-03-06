from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils


import os
import json
import argparse
import timeit

start_time = timeit.default_timer()

parser = argparse.ArgumentParser(description='Calculate the model for CNN keras')
parser.add_argument('--nb_filters', dest='nb_filters', type=int, default=32)
parser.add_argument('--nb_pool', dest='nb_pool', type=int, default=2)
parser.add_argument('--nb_conv', dest='nb_conv', type=int, default=3)
parser.add_argument('--nb_epoch', dest='nb_epoch', type=int, default=12)

parser.add_argument('--_id', dest='_id', default=None)
params = vars(parser.parse_args())

batch_size = 128
nb_classes = 10
nb_epoch = params['nb_epoch']

# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = params['nb_filters']
# size of pooling area for max pooling
nb_pool = params['nb_pool']
# convolution kernel size
nb_conv = params['nb_conv']

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                        border_mode='valid',
                        input_shape=(1, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
#print('Test score:', score[0])
#print('Test accuracy:', score[1])
end_time = timeit.default_timer()
cost_time = end_time - start_time

# Save result
_id = params['_id']
if not os.path.exists(_id):
    os.makedirs(_id)
with open(os.path.join(_id, 'value.json'), 'w') as outfile:
    json.dump({'_scores': {'score': score[0],'accuracy':score[1], 'time':cost_time}}, outfile)