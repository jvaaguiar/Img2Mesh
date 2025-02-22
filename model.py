from tensorflow.keras import models, layers
import tensorflow.keras.backend as K
import tensorflow as tf
from tensorflow.keras.constraints import MaxNorm


# ==============================================================================
# the architecture that gave the best results !!!!!
# convolutional feature filter works well for silhouettes
def createLeanNetwork(hidden_size, out_vertices):
    model = models.Sequential()
    model.add(layers.MaxPooling2D((4, 4), data_format='channels_first', input_shape=(1, 400, 400)))
    model.add(layers.Conv2D(16, (3,3), data_format='channels_first'))
    model.add(layers.MaxPooling2D((3, 3), data_format='channels_first'))
    model.add(layers.Conv2D(48, (3,3), data_format='channels_first'))
    model.add(layers.MaxPooling2D((3, 3), data_format='channels_first'))
    model.add(layers.Conv2D(72, (3,3), data_format='channels_first'))
    model.add(layers.Conv2D(72, (3,3), data_format='channels_first'))
    model.add(layers.MaxPooling2D((3, 3), data_format='channels_first'))

    model.add(layers.Flatten())
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(hidden_size, activation='relu'))

    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(hidden_size / 2, activation='relu'))

    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(3 * out_vertices, activation='tanh'))
    model.add(layers.Reshape((out_vertices, 3)))

    return model


# ==============================================================================
# convolutional network inspired in the VGG-16 architecture
def createNetwork(hidden_size, out_vertices):
    model = models.Sequential()
    model.add(layers.Conv3D(64, (2,3,3), input_shape=(6, 400, 400, 1)))
    model.add(layers.Conv3D(64, (1,3,3)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(128, (2,3,3)))
    model.add(layers.Conv3D(128, (1,3,3)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(256, (2,3,3)))
    model.add(layers.Conv3D(256, (1,4,4)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(512, (2,3,3)))
    model.add(layers.Conv3D(512, (1,3,3)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(1024, (2,3,3)))
    model.add(layers.Conv3D(1024, (1,3,3)))

    model.add(layers.Flatten())
    model.add(layers.Dense(hidden_size, activation='relu'))
    model.add(layers.Dense(3 * out_vertices))
    model.add(layers.Reshape((out_vertices, 3)))

    return model


# ==============================================================================
# OUTPUT ALWAYS (50, 3)
def createDeconvNetwork():
    model = models.Sequential()
    model.add(layers.Conv3D(64, (2,3,3), input_shape=(6, 400, 400, 1)))
    model.add(layers.Conv3D(64, (1,3,3)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(128, (2,3,3)))
    model.add(layers.Conv3D(128, (1,3,3)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(256, (2,3,3)))
    model.add(layers.Conv3D(256, (1,4,4)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(512, (2,3,3)))
    model.add(layers.Conv3D(512, (1,3,3)))
    model.add(layers.MaxPooling3D((1, 2, 2)))
    model.add(layers.Conv3D(1024, (2,3,3)))
    model.add(layers.Conv3D(1024, (1,4,4)))
    model.add(layers.MaxPooling3D((1, 2, 2)))

    model.add(layers.Reshape((8, 8, 1024)))

    model.add(layers.Conv2D(1024, (3,3)))
    model.add(layers.Conv2DTranspose(3, (15,15)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(3, (3,3)))
    model.add(layers.Reshape((8 * 8, 3)))
    model.add(layers.Conv1D(3, (15)))

    return model
