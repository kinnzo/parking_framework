import cv2
import numpy as np

global path

def get_hist(image):
	chans = cv2.split(image)
	colors = ("b", "g", "r")
	features = []
	for (chan, color) in zip(chans, colors):
		hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
		features.extend(hist)
	return features

def dist_check(f1,f2):
	d = cv2.compareHist(np.asarray(f1), np.asarray(f2), cv2.HISTCMP_BHATTACHARYYA)
	return d

def mark(box,image):
	global path
	overlay = image.copy()
	cv2.rectangle(overlay, (box[2][0], box[1][0]), (box[2][1], box[1][1]), (0, 200, 0), -1)  # A filled rectangle
	alpha = 0.4  # Transparency factor.
	# Following line overlays transparent rectangle over the image
	image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
	#cv2.imwrite(out_name,image_new)
	return image_new

def similarity(fno,lfno,bboxes,flist,llist):
	fname = path + "%(#)06d.jpg" %{"#":fno}
	lname = path + "%(#)06d.jpg" %{"#":lfno}
	print fname + lname
	img1 = cv2.imread(fname)
	img2 = cv2.imread(lname)
	ctr = 0
	for cframe in flist:
		for lframe in llist:
			if abs(cframe[0]-lframe[0]) < 16 and abs(cframe[1]-lframe[1]) < 16:
				for box in bboxes:
					if abs(cframe[0]-box[2][0]) < 16 and abs(cframe[1]-box[1][0]) < 16:
						im1 = img1[box[1][0]:box[1][1],box[2][0]:box[2][1]]
						im2 = img2[box[1][0]:box[1][1],box[2][0]:box[2][1]]
						h1 = get_hist(im1)
						h2 = get_hist(im2)
						if dist_check(h1,h2) < 0.25:
							img1 = mark(box,img1)
							ctr = ctr + 1
	out_name = "./frames/out/out_" +  "%(#)06d.jpg" %{"#":fno}
	lbl1 = "Number of slots = " + str(len(bboxes))
	lbl2 = "Number of slots occupied = " + str(ctr)
	cv2.putText(img1, str(lbl1), (1350,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
	cv2.putText(img1, str(lbl2), (1350,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
	cv2.imwrite(out_name,img1)

if __name__ == "__main__":
	global path
	path = "./frames/frames/"
	file = open("8_30-meta.info","r")
	#last_fno = -1
	#print('')
	bboxes = []
	for line in file:
		field = line.split(",")
		fno = int(field[0])
		bbox = [[fno],[int(field[2]),int(field[2]) + int(field[4])],[int(field[1]),int(field[1]) + int(field[3])]]
		bboxes.append(bbox)
	print('[INFO] Bounding Boxes:')
	print bboxes
	file.close()
	file = open("det.txt","r")
	last_fno = -1
	print('')
	f_list = []
	last_list = []
	for line in file:
		field = line.split(",")
		#print(int(field[0])," ",int(field[1])," ",float(field[2])," ",float(field[3])," ",float(field[4])," ",float(field[5]))
		if last_fno == -1:
			last_fno = int(field[0])
		fno = int(field[0])
		if fno != last_fno:
			similarity(fno,last_fno,bboxes,f_list,last_list)
			last_fno=fno
			last_list = f_list
			f_list=[]
		frame = [float(field[2]),float(field[3]),float(field[4]),float(field[5])]
		f_list.append(frame)
	file.close()
