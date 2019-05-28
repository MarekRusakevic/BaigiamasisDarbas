import keras
from keras.utils import to_categorical
import numpy as np
from PIL import Image
import os
from matplotlib import pyplot as plt
from keras.models import model_from_json

# Ikelti modelį ir svorius


json_file = open('SavedModel/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# Ikelti svorius į modelį
loaded_model.load_weights("SavedModel/model.h5")
print("Loaded model from disk")

loaded_model.compile(optimizer='adamax', loss='categorical_crossentropy', metrics=['accuracy'])

# Guess

img = Image.open('guess.png')
img.load()

k = np.array(img)

img_size = len(k)

y = k.reshape(1,img_size,img_size,1)

prediction = loaded_model.predict(y)

prediction = np.array(prediction).tolist()

max_value = max(prediction[0])

max_index = prediction[0].index(max_value)

letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

if(letter[max_index] == 'A'):
      print('Atsakymas: Brick 2x2')
elif (letter[max_index] == 'B'):
      print('Atsakymas: Brick 1x2')
elif (letter[max_index] == 'C'):
      print('Atsakymas: Brick 1x1')
elif (letter[max_index] == 'D'):
      print('Atsakymas: Plate 2x2')	  
elif (letter[max_index] == 'E'):
      print('Atsakymas: Plate 1x2')
elif (letter[max_index] == 'F'):
      print('Atsakymas: Plate 1x1')	 
elif (letter[max_index] == 'G'):
      print('Atsakymas: Roof Tile 1x2x45deg')
elif (letter[max_index] == 'H'):
      print('Atsakymas: Half bush')	  
	  
	  
#print('Atsakymas: ' + letter[max_index])