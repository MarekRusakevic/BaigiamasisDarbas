import keras
from keras.models import Model
from keras.layers import Input, Dense, Dropout
from keras.layers import Reshape, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
import numpy as np
from PIL import Image
import os
from matplotlib import pyplot as plt

from keras.preprocessing.image import ImageDataGenerator

data = np.genfromtxt('SavedModel/training.csv', delimiter=',')
data = data[1:][:,1:]

fig, axes = plt.subplots(1, 1)

axes.plot(data[:,0]) # training accuracy
axes.plot(data[:,2]) # testing accuracy
axes.legend(['Training', 'Testing'])
axes.set_title('Accuracy Over Time')
axes.set_xlabel('epoch')
axes.set_ybound(0.0, 1.0)

plt.show()	