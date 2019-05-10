import numpy as np
import cv2
import glob
import os

image_dir = './all/'
glob_arg = image_dir + "/*.jpg"
glob_list = glob.glob(glob_arg)
glob_list.sort()

fctr=0
for fname in glob_list:
	img = cv2.imread(fname)
	imA ="./A/"+"%(#)06d.jpg" %{"#":fctr}
	imB ="./B/"+"%(#)06d.jpg" %{"#":fctr}
	imC ="./C/"+"%(#)06d.jpg" %{"#":fctr}
	imD ="./D/"+"%(#)06d.jpg" %{"#":fctr}
	imE ="./E/"+"%(#)06d.jpg" %{"#":fctr}
	imF ="./F/"+"%(#)06d.jpg" %{"#":fctr}
	imG ="./G/"+"%(#)06d.jpg" %{"#":fctr}
	imH ="./H/"+"%(#)06d.jpg" %{"#":fctr}
	fctr = fctr + 1

	imgA = img[0:360,0:320]
	cv2.resize(imgA,(640,720))
	cv2.imwrite(imA,imgA)

	imgB = img[0:360,320:640]
	cv2.resize(imgB,(640,720))
	cv2.imwrite(imB,imgB)
	
	imgC = img[0:360,640:960]
	cv2.resize(imgC,(640,720))
	cv2.imwrite(imC,imgC)
	
	imgD = img[0:360,960:1280]
	cv2.resize(imgD,(640,720))
	cv2.imwrite(imD,imgD)

	imgE = img[360:720,0:320]
	cv2.resize(imgE,(640,720))
	cv2.imwrite(imE,imgE)

	imgF = img[360:720,320:640]
	cv2.resize(imgF,(640,720))
	cv2.imwrite(imF,imgF)
	
	imgG = img[360:720,640:960]
	cv2.resize(imgG,(640,720))
	cv2.imwrite(imG,imgG)
	
	imgH = img[360:720,960:1280]
	cv2.resize(imgH,(640,720))
	cv2.imwrite(imH,imgH)
