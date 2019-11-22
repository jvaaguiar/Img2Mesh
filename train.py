import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from model import createNetwork
from optimizer import Optimizer
from prepare_data import prepareData

import tensorflow as tf
import numpy        as np

def testTrain():
    net = createNetwork(100, 50)
    optim = Optimizer(net)

    X, Y = prepareData()
    X = tf.constant(X, shape=[len(X), 6, 400, 400, 1])
    return X