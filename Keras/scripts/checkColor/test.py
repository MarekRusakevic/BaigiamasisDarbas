from scipy.misc import imread, imsave, imresize
image = imread('test.png')
if(len(image.shape)<3):
      print ('gray')
elif len(image.shape)==3:
      print ('Color(RGB)')
else:
      print ('others')