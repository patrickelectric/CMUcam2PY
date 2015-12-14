import serial
import random
import numpy as np
import matplotlib.pyplot as plt

#ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)

#while(True):

#	if(ser.read(87)=='\n'):
#		print "ae"

image = [[[0,0,1],[0,0,1],[1,0,0]] for i in xrange(3)]
print image
plt.imshow(image)
plt.show()

image = [[1,0,0] for i in xrange(1)]
plt.matshow(image,cmap=plt.cm.gray)
#plt.show()

image = np.random.rand(87,87)
plt.matshow(image,cmap=plt.cm.gray)
#plt.show()