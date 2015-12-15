import sys
import time
import scipy
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=115200)

rgbinit = [125,125,125,125,125,125]

def map(x,in_min=16,in_max=240,out_min=0,out_max=250):
	return abs((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

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
image=[]

def onclick(event):
    # print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
	x=event.xdata
	y=event.ydata
	print 'X=%f, y=%f'%(x,y)
	if(x>2 and x<87 and y>2 and y<87):
		global image
		print len(image)
		rgb = image[int(y)][int(x)]
		global rgbinit
		rgbinit=[rgb[0]+25,rgb[0]-25,rgb[1]+25,rgb[1]-25,rgb[2]+25,rgb[2]-25]
		for i in range(len(rgbinit)):
			if(rgbinit[i]<0):
				rgbinit[i]=0
			if(rgbinit[i]>255):
				rgbinit[i]=255
		print rgbinit


def imagehold(image,rgbv):
	xsize = len(image)
	ysize = len(image[0])
	newimage=[]
	for i in range (len(image)):
		row=[]
		for o in range(len(image[0])):
			pixel=[]
			for u in range(len(image[0][0])):
				if (image[i][o][u] > rgbv[2*u]):
					pixel.append(np.uint8(1))
				else:
					if (image[i][o][u] < rgbv[2*u+1]):
						pixel.append(np.uint8(1))
					else:
						pixel.append(np.uint8(254))
			row.append(pixel)
			print pixel
		newimage.append(row)
	return newimage



	image

slicechange=True

def sliceupdateRmax(val):
	rgbinit[0]=val

def sliceupdateRmin(val):
	rgbinit[1]=val

def sliceupdateGmax(val):
	rgbinit[2]=val

def sliceupdateGmin(val):
	rgbinit[3]=val

def sliceupdateBmax(val):
	rgbinit[4]=val

def sliceupdateBmin(val):
	rgbinit[5]=val

fig,sub = plt.subplots(2,2)
fig.canvas.mpl_connect('button_press_event', onclick)

ser.write("RS \r")
time.sleep(0.5);
ser.write("FS 1 \r")
time.sleep(0.1)
ser.write("SF \r")

ff=0
while True :
	print 'waiting image..'
	while take(1)!=1:
		pass

	print 'size'
	size = take(2)
	print size

	image_data=[]
	for x in xrange(1,87):
		data = takeuntil(2)
		image_data.append([[255-map(data[i]),255-map(data[i+1]),255-map(data[i+2])] for i in range(0, len(data), 3)])

	image=image_data
	#image=np.array(image)
	sub[0][0].imshow(image)
	sub[0][1].imshow(imagehold(image,rgbinit))
	sub[1][1].imshow(image)
	#sub[0].axis([0,87,0,87])
	if(ff==0):
		sub[1][0].plot()
		sub[1][0].axis([-1,-1.1,-1,-1.1])
		#sub[1].axis([-])
		axcolor = 'lightgoldenrodyellow'
		Rmax = plt.axes([0.2, 0.1, 0.20, 0.03], axisbg=axcolor)
		Rmin = plt.axes([0.2, 0.15, 0.20, 0.03], axisbg=axcolor)
		Gmax = plt.axes([0.2, 0.2, 0.20, 0.03], axisbg=axcolor)
		Gmin = plt.axes([0.2, 0.25, 0.20, 0.03], axisbg=axcolor)
		Bmax = plt.axes([0.2, 0.3, 0.20, 0.03], axisbg=axcolor)
		Bmin = plt.axes([0.2, 0.35, 0.20, 0.03], axisbg=axcolor)

		RmaxV = Slider(Rmax, 'Rmax', 1, 254, valinit=rgbinit[0])
		RminV = Slider(Rmin, 'Rmin', 1, 254, valinit=rgbinit[1])
		GmaxV = Slider(Gmax, 'Gmax', 1, 254, valinit=rgbinit[2])
		GminV = Slider(Gmin, 'Gmin', 1, 254, valinit=rgbinit[3])
		BmaxV = Slider(Bmax, 'Bmax', 1, 254, valinit=rgbinit[4])
		BminV = Slider(Bmin, 'Bmin', 1, 254, valinit=rgbinit[5])

		RmaxV.on_changed(sliceupdateRmax)
		RminV.on_changed(sliceupdateRmin)
		GmaxV.on_changed(sliceupdateGmax)
		GminV.on_changed(sliceupdateGmin)
		BmaxV.on_changed(sliceupdateBmax)
		BminV.on_changed(sliceupdateBmin)

		ff=1
	else:
		RmaxV.set_val(rgbinit[0])
		RminV.set_val(rgbinit[1])
		GmaxV.set_val(rgbinit[2])
		GminV.set_val(rgbinit[3])
		BmaxV.set_val(rgbinit[4])
		BminV.set_val(rgbinit[5])

		print rgbinit

	plt.pause(0.1)
	plt.show(block=False)
	#print samp.val,sfreq.val
