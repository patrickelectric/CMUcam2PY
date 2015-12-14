import serial
import random
import numpy as np
import matplotlib.pyplot as plt

# 1 Xsize Ysize 2 r g b r g b ... r g b r g b 2 r g b r g b ... r g b r g b 3
# 1 - new frame 2 - new row 3 - end of frame
# RGB (CrYCb) ranges from 16 - 240
# RGB (CrYCb) represents two pixels color values. Each pixel shares the red and blue.
# 176 cols of R G B (Cr Y Cb) packets (forms 352 pixels)
# 144 rows
# To display the correct aspect ratio, double each column so that your final image is 352x144

string = [1,3,3,2,1,0,0,0,1,0,0,0,1,2,0,1,0,0,0,1,1,0,0,2,0,0,1,1,0,0,0,1,0,3]

for i in range(10):
	if string[i]==1:
		xsize = string[i+1];
		ysize = string[i+2];
		if string[i+3]==2:
			i+=4
			print string[i:]
