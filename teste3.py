import sys
import scipy
import serial
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=57600)

def take(x):
	if(x==1):
		return ord(ser.read())
	else:
		return [ord(ser.read()) for i in range(x)]

def takeuntil(x):
	a = []
	char = 0
	count = 0
	while(True):
		char = take(1)
		if(char!=x):
			a.append(char)
		else:
			return a

while True :
	print 'waiting image..'
	while take(1)!=1:
		pass		

	print 'size'
	size = take(2)	
	print size

	image=[]
	for x in xrange(1,size[0]):
		data = takeuntil(2)
		image.append([[255-data[i],255-data[i+1],255-data[i+2]] for i in range(0, len(data), 3)])
	


	image=np.array(image)
	
	plt.imshow(image)
	plt.show(block=False)
	plt.draw()
 	plt.pause(0.1)

 	
