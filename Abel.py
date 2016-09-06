import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from numpy import array
from PIL import ImageStat
import math
from pylab import *

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'
cmap = matplotlib.cm.jet
norm = matplotlib.colors.Normalize(vmin = 0,vmax=360)

path='E:\\flame image\\stratified flame\\S0012'
filename=os.listdir(path)
retval = os.getcwd()
print("Current working directory %s" % retval)
os.chdir(path)

imarray=array(Image.open("output.bmp"))

Rows,Columes=imarray.shape
print Rows,Columes

Num = 352
a = imarray[:,Num:704]
b = a[:,352:0:-1]
P = np.hstack((b,a))
M = 703
N = 704

I_zero=np.zeros((N,N))
for i in range(N):
	for j in range(N):
		if(j<i or j==i==0):
			I_zero[i,j]=0
		elif(i==j!=0):
			I_zero[i,j]=1.0/(2.0*np.pi)*math.log((math.sqrt((2*j+1)**2-4*(i**2))+2*j+1)/(2*j))
		elif(j>i):
			I_zero[i,j]=1.0/(2.0*np.pi)*math.log((math.sqrt((2*j+1)**2-4*(i**2))+2*j+1)/(math.sqrt((2*j-1)**2-4*(i**2))+2*j-1))

I_one=np.zeros((N,N))
for i in range(N):
	for j in range(N):
		if(j<i):
			I_one[i,j]=0
		elif(j==i):
			I_one[i,j]=1.0/(2.0*np.pi)*math.sqrt((2*j+1)**2-4*(i**2))-2*j*I_zero[i,j]
		else:
			I_one[i,j]=1.0/(2.0*np.pi)*(math.sqrt((2*j+1)**2-4*(i**2))-math.sqrt((2*j-1)**2-4*(i**2)))-2*j*I_zero[i,j]

D=np.zeros((M,M))
for i in range(M):
	for j in range(M):
		if(j<i-1):
			D[i,j]=0
		elif(j==i-1):
			D[i,j]=I_zero[i,j+1]-I_one[i,j+1]
		elif(j==i):
			D[i,j]=I_zero[i,j+1]-I_one[i,j+1]+2*I_one[i,j]
		elif(i==0 and j==1):
			D[i,j]=I_zero[i,j+1]-I_one[i,j+1]+2*I_one[i,j]-2*I_one[i,j-1]
		elif(j>i+1 or j==i+1):
			D[i,j]=I_zero[i,j+1]-I_one[i,j+1]+2*I_one[i,j]-I_zero[i,j-1]-I_one[i,j-1]

f=np.zeros((Rows,M))
for i in range(Rows):
	f[i,:]=1000*np.dot(D,P[i,:])
im=Image.fromarray(f)
plt.imshow(f[:,352:704],cmap=cmap,norm=norm)
if im != 'RGB':
    im = im.convert('RGB')
img=im.save("result.bmp")
plt.axis('off')
plt.colorbar()
plt.show()

