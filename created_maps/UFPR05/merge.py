import numpy as np
import cv2
import glob
import os

#imA = cv2.imread('')

def map_merger(image_dir):
	#image_dir = './sunny_30/'
	glob_arg = image_dir + "/*.jpg"	
	glob_list = glob.glob(glob_arg)
	glob_list.sort()
	imA = cv2.imread(glob_list[0])
	imB = cv2.imread(glob_list[1])
	imC = cv2.imread(glob_list[2])
	imD = cv2.imread(glob_list[3])
	imE = cv2.imread(glob_list[4])
	imF = cv2.imread(glob_list[5])
	imG = cv2.imread(glob_list[6])
	imH = cv2.imread(glob_list[7])

	v1 = np.concatenate((imA,imB,imC,imD),axis=1)
	v2 = np.concatenate((imE,imF,imG,imH),axis=1)
	v = np.concatenate((v1,v2),axis=0)
	out_name = image_dir + ".jpg"
	cv2.imwrite(out_name,v)

map_merger('./sunny_30')
map_merger('./sunny_60')
map_merger('./cloudy_30')
map_merger('./cloudy_60')
map_merger('./rainy_30')
map_merger('./rainy_60')

