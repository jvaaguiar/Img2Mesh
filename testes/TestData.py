import numpy as np
import tensorflow as tf

# CREATE DATA
y0 = [
      [-1.0,+1.0,-1.0],
      [+1.0,+1.0,-1.0],
      [+0.0,-1.0,-1.0],
      [+0.0,+0.0,+1.0],
      [-1.0,+1.0,-1.0], # remove v
      [+1.0,+1.0,-1.0],
      [+0.0,-1.0,-1.0],
      [+0.0,+0.0,+1.0]
]

y1 = [
      [-1.0,+1.0,-1.0],
      [+1.0,+1.0,-1.0],
      [+1.0,-1.0,-1.0],
      [-1.0,-1.0,-1.0],
      [-1.0,+1.0,+1.0],
      [+1.0,+1.0,+1.0],
      [+1.0,-1.0,+1.0],
      [-1.0,-1.0,+1.0]
]

y2 = [
      [-1.0,+1.0,+0.0],
      [+1.0,+1.0,+0.0],
      [+1.0,-1.0,+0.0],
      [-1.0,-1.0,+0.0],
      [+0.0,+0.0,+1.0],
      [+0.0,+0.0,-1.0],
      [+0.0,+0.0,+1.0], # remove v
      [+0.0,+0.0,-1.0],
]

y3 = [
      [-1.0,+1.0,-1.0],
      [+1.0,+1.0,-1.0],
      [+1.0,-1.0,-1.0],
      [-1.0,-1.0,-1.0],
      [+0.0,+1.0,+1.0],
      [+0.0,-1.0,+1.0]
]

X = [0.0, 1.0, 2, 3]
Y = [y0, y1, y2, y3]


# NORMALIZE DATA
norm_X = np.array((X - np.min(X))/(np.max(X) - np.min(X)))
norm_Y = []
for y in Y:
  norm_Y.append((np.array(y).flatten() - np.min(y)) / (np.max(y) - np.min(y)))


tensor_X = tf.constant(norm_X, shape = [4,1])
tensor_Y = tf.ragged.constant(norm_Y)