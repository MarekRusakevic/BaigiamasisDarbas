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


X = []
labels = []
DATA_PATH = 'images'
# Kiekvienam aplankui
for directory in os.listdir(DATA_PATH):
    # Kiekvienam paveikslėliui
    for image in os.listdir(DATA_PATH + '/' + directory):
        # Atidaryti paveikslėli ir išsaugoti į masyvą
        try:
            file_path = DATA_PATH + '/' + directory + '/' + image
            img = Image.open(file_path)
            img.load()  
	
            img_data = np.asarray(img, dtype=np.int16)
            # Pridėti paveikslėli prie dataset'o
            X.append(img_data)
            # Pridėti žymėjimą
            labels.append(directory)
        except:
            None # Jeigu neišėjo pakraut
N = len(X) # Paveikslėliu kiekis

img_size = len(X[0]) # Paveikslėlio dydis

X = np.asarray(X).reshape(N, img_size, img_size, 1)

##########

labels = to_categorical(list(map(lambda x: ord(x)-ord('A'), labels)), 8)

# Sumaišom visus duomenis, ir padalinam juos i testavimo ir mokymo

temp = list(zip(X, labels))
np.random.shuffle(temp)
X, labels = zip(*temp)
X, labels = np.asarray(X), np.asarray(labels)
PROP_TRAIN = 0.7 # proporcija paveikslėliu skirtas mokymui
NUM_TRAIN = int(N * PROP_TRAIN) # keikis paveikslėliu skirtas mokymui
X_train, X_test = X[:NUM_TRAIN], X[NUM_TRAIN:]
labels_train, labels_test = labels[:NUM_TRAIN], labels[NUM_TRAIN:]


# Konstruojam modelį


shape = X[0].shape
img_in = Input(shape=shape, name='input')

x = Conv2D(32, (3,3), activation='selu', name='block1_conv1')(img_in)
x = MaxPooling2D((2,2), name='block1_pool')(x)

x = Flatten(name='block3_flatten')(x)

x = Dense(128, activation='selu', name='block3_dense1')(x)

x = Dropout(0.5, name='block1_dropout1')(x)

x = Dense(64, activation='selu', name='block3_dense2')(x)

output = Dense(8, activation='softmax', name='output')(x)


# Kompiliuojam
model = Model(img_in, output)
#model.compile(optimizer='sgd',
model.compile(optimizer='adamax',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# Paleidžiam 40 iteraciju

csv_logger = keras.callbacks.CSVLogger('SavedModel/training.csv', append=True)

# train 
model.fit(X_train, labels_train,
          epochs=40, batch_size=64,
          validation_data=[X_test, labels_test],
          callbacks=[csv_logger])


# Išsaugom modelį ir jo svorius		  
		  
model_json = model.to_json();
with open("SavedModel/model.json", "w") as json_file:
	json_file.write(model_json)

model.save_weights("SavedModel/model.h5")
print("Saved model to disk")
		  

		  
# Grafas	  

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


# Surandam modelio tikimybe atpažinti

score = model.evaluate(X_test, labels_test, verbose=False)
print('Loss: {}'.format(score[0]))
print('Accuracy: {}%'.format(np.round(10000*score[1])/100))

