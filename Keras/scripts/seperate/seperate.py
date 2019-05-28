import os
from PIL import Image
import random

source = 'img'
test = 'test/'
train = 'train/'

for image in os.listdir(source):
	file_path = source + '/' + image
	img = Image.open(file_path)
	img.load()
	x = random.randint(1,101)
	
	if(x < 71):
		img.save(train + image)
	else:
		img.save(test + image)
