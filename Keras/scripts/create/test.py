
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import scipy.ndimage as ndimage

#datagen = ImageDataGenerator(rotation_range=10, width_shift_range=0.1, 
#height_shift_range=0.1,shear_range=0.15, 
#zoom_range=0.1,channel_shift_range = 10, horizontal_flip=True)

datagen = ImageDataGenerator(
          featurewise_center=False, 
          featurewise_std_normalization=False, 
          width_shift_range=0.1,
          height_shift_range=0.1,
          zoom_range=0.2,
          shear_range=0.1,
          rotation_range=10.,
          )


image_path = 'load.png'

image = np.expand_dims(ndimage.imread(image_path), 0)

save_here = 'saved'

datagen.fit(image)

for x, val in zip(datagen.flow(image,                    #image we chose
	save_to_dir=save_here,     #this is where we figure out where to save
	save_prefix='aug',        # it will save the images as 'aug_0912' some number for every new augmented image
	save_format='png'),range(10)) :     # here we define a range because we want 10 augmented images otherwise it will keep looping forever I think
	pass