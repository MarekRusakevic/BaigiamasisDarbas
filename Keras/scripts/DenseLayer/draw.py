import numpy as np
from matplotlib import pyplot as plt

# Grafas	  

data = np.genfromtxt('RecognChance.csv', delimiter=',')

data = data[1:][:,0:]

fig, axes = plt.subplots(1,1)

axes.plot(data[:,1]) # training accuracy
axes.plot(data[:,2]) # testing accuracy
axes.legend(['Training', 'Testing'])
axes.set_title('Accuracy depending on neuron amount')

axes.set_xlabel('Neurons')
axes.set_xticks([0,1,2,3,4,5])
axes.set_xticklabels( ('16', '32','64','128','256','512') )

plt.show()