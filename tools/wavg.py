#from skvideo.io import VideoWriter
import cv2
import numpy as np
import glob

def modify(fname):
	foreground = cv2.imread(fname)
	background = cv2.imread(fname)
	alpha = cv2.imread("8_30.jpg")
	# Convert uint8 to float
	foreground = foreground.astype(float)
	background = background.astype(float)
	# Normalize the alpha mask to keep intensity between 0 and 1
	alpha = alpha.astype(float)/255
	foreground = cv2.multiply(alpha, foreground)
	background = cv2.multiply((1.0 - alpha)*0.2, background)
	outImage = cv2.add(foreground, background)
	return outImage

glob_arg = "./frames/frames/*.jpg"
glob_list = glob.glob(glob_arg)
glob_list.sort()

img_array = []
i=0
w=0
h=0
size = (1920, 1080)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('custom_test.avi',fourcc, 4.0,size)
count = 0
for fname in glob_list:
    #i=i+1
    print fname
    #if i > 100:
    #    break
    img_array.append(np.uint8(modify(fname)))
    out.write(img_array[i])
    count += 1
    if(count > 100):
        break
#for i in range(len(img_array)):
#    out.write(img_array[i])
    #writer.write(img_array[i])
#writer.release()
out.release()
