import os
from PIL import Image

source = 'images'
save = 'save/'

for image in os.listdir(source):
	file_path = source + '/' + image
	img = Image.open(file_path)
	img.load()
	img = img.convert('L')
	img = img.resize((100, 100), Image.ANTIALIAS)
	img.save(save + image)