import keras
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.optimizers import RMSprop

from automl.mltask.tasknode.basenode import BaseNode
import numpy as np


class DLSeqNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        f = np.load(self.inpath[0])
        x_train, y_train, x_test, y_test = f['x_train'], f['y_train'], f['x_test'], f['y_test']

        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255

        y_train = keras.utils.to_categorical(y_train, 10)
        y_test = keras.utils.to_categorical(y_test, 10)

        model = Sequential()
        for layer in self.config.get('layerStruct'):
            add_layer(model, layer)

        model.summary()
        model.compile(loss=self.config.get('compileParams').get('loss'),
                      optimizer=self.config.get('compileParams').get('optimizer'),
                      metrics=['accuracy'])

        history = model.fit(x_train, y_train,
                            batch_size=int(self.config.get('trainParams').get('batch_size')),
                            epochs=int(self.config.get('trainParams').get('epochs')),
                            verbose=1,
                            validation_data=(x_test, y_test))
        score = model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config


def add_layer(model, layer):
    params = {}
    for param in params_list:
        if layer.get(param):
            try:
                params[param] = eval(layer.get(param))
            except NameError:
                params[param] = layer.get(param)
    if layer['name'][1] == 'Dense':
        model.add(Dense(**params))
    elif layer['name'][1] == 'Activation':
        model.add(Activation(**params))
    elif layer['name'][1] == 'Dropout':
        model.add(Dropout(**params))
    elif layer['name'][1] == 'Flatten':
        model.add(Flatten(**params))
    elif layer['name'][1] == 'Conv2D':
        model.add(Conv2D(**params))
    elif layer['name'][1] == 'MaxPooling2D':
        model.add(MaxPooling2D(**params))


params_list = ['input_shape', 'activation', 'filters', 'kernel_size', 'units', 'filters', 'pool_size', 'rate']
