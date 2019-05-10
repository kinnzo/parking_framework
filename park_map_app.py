from numpy import genfromtxt
import argparse
import numpy as np
import cv2
import glob
import os
import subprocess

class TrackID:
	def __init__(self,fid,vid,x,y,w,b):
		self.fid=fid
		self.vid = vid
		self.x = x
		self.y = y
		self.w = w
		self.b = b
	lost = 0
	frame = 1
	seen = -1

id_list=[]
global arr 
global arr_map
global meta_file
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def add_to_map(veh):
	global arr
	global arr_map
	global meta_file
	#if abs((veh.w//16) * (veh.b//16)) > 50:
	#	return
	height = arr.shape[0]
	width = arr.shape[1]
	print("[ADDING] Vehicle ID: "),
	print(veh.vid),
	print(", Number of Frames: "),
	print(veh.frame)
	bx=int(veh.x)
	by=int(veh.y)
	bw=bx + int(veh.w)
	bh=by + int(veh.b)
	f = open(meta_file,"r")
	flag = 1
	for line in f:
		data = [int(i) for i in line.split(",") if i.isdigit()]
		print(data)
		if len(data) > 3:
			if abs(veh.x - data[1]) < 16:
				flag = 0
				break
			elif abs(veh.y - data[2]) < 16:
				flag = 0
				break
	f.close()
	if flag == 1:
		f = open(meta_file,"a")
		f.write(str(int(veh.vid)) + "," + str(int(veh.x)) + "," + str(int(veh.y)) + "," + str(int(veh.w)) + "," + str(int(veh.b))+ "\n")
		f.close()
        if bx < 0:
            bx = 0
        if by < 0:
            by = 0
        if bw >= width:
            bw = width - 1
        if bh >= height:
            bh = height - 1
	print("[MARKING] X1: "),
	print(bx),
	print(", X2: "),
	print(bw),
	print(", Y1: "),
	print(by),
	print(", Y2: "),
	print(bh)
	for i in range(bx,bw):
		for j in range(by,bh):
			arr[j][i]=1
	for i in range(bx//16,bw//16):
		for j in range(by//16,bh//16):
			arr_map[j][i]= abs((veh.w//16) * (veh.b//16))

def mark_areas(frame_ids,motion_t,lot_t):
	global id_list
	#print("Frame IDs :"),
	#for i in frame_ids:
	#	print(i.fid,"&",i.vid),
	#print("")
	#print("ID_List :"),
	#for j in id_list:
	#	print(j.fid,"&",j.vid),
	#print("done")
	#print(" ")

	for i in frame_ids:
		for j in id_list:
			#print(i.vid," , ",j.vid)
			if i.vid == j.vid:
				if abs(j.x - i.x) < motion_t and abs(j.y - i.y) < motion_t:
					j.frame = j.frame + 1
					j.seen = 0
				else:
					if j.frame > lot_t:
						add_to_map(j)
					print("[REMOVING] Moving Vehicle ID: "),
					print(j.vid),
					print(", Initial Y: "),
					print(j.y),
					print(", Final Y: "),
					print(i.y)
					print('')
					id_list.remove(j)
				#frame_ids.remove(i)
	tmp_list = []
	for j in id_list:
		if j.seen == -1:
			j.lost = j.lost + 1
		if j.lost > 3:
			if j.frame > lot_t:
				add_to_map(j)
			print("[REMOVING] Lost Vehicle ID: "),
			print(j.vid),
			print(", Number of Frames: "),
			print(j.frame),
			print(", Absent in Frames: "),
			print(i.y)
			print('')
			#id_list.remove(j)
		else:
			tmp_list.append(j)
	id_list = tmp_list

	for i in frame_ids:
		f=0
		for j in id_list:
			if i.vid == j.vid:
				f=1
				break
		if f==0:
			id_list.append(i)

	for j in id_list:
		j.seen = -1


def create_seq_data(i,image_dir):
	with cd("./tools/deep_sort/"):
		if not(os.path.exists("tmp")):
			os.system("mkdir tmp")

	with cd("./tools/deep_sort/tmp"):
		if not(os.path.exists("SeqData")):
			os.system("mkdir SeqData")

	with cd("./tools/deep_sort/tmp/SeqData"):
		try:
			os.remove("seqinfo.ini")
		except OSError:
			pass
		img_loc = "imDir"+image_dir
		seqLen = "seqLength="+str(i)
		f1 = open("seqinfo.ini","w")
		f1.write("[Sequence]\n")
		f1.write("name=custom\n")
		f1.write(img_loc)
		f1.write("\n")
		f1.write("frameRate=4\n")
		f1.write(seqLen)
		f1.write("\n")
		f1.write("imWidth=640\n")
		f1.write("imHeight=720\n")
		f1.write("imExt=.jpg\n")
		f1.close()
	with cd("./tools/deep_sort/tmp/SeqData"):
		if not os.path.exists("det"):
			os.system("mkdir det")

def parseArgs():
	parser = argparse.ArgumentParser(description="Auto Parking Map Generator")
	parser.add_argument( "--image_dir", help="Path to Image Directory",
        default="./data/images", required=False)
	parser.add_argument( "--motion_thresh", help="Maximum Permissible vehicle movement",
        default=16, required=False, type=float)
	parser.add_argument( "--lot_thresh", help="Number of frames to make it a parking lot",
        default=3, required=False, type=int)
	parser.add_argument("--output_file", help="Enter a name for the output file",default="park_map",required=False)
	return parser.parse_args()
		

if __name__ == "__main__":
	global arr
	global arr_map
	global meta_file
	#arr = np.zeros((1920,1080))
	args = parseArgs()
	glob_arg = args.image_dir + "/*.jpg"
	#print(glob.glob(glob_arg))
	meta_file = args.output_file + "-meta.info"
	try:
		os.remove(meta_file)
	except OSError:
		pass
	meta = open(meta_file,"w")
	meta.write("id,x,y,w,b\n")
	meta.close()
	glob_list = glob.glob(glob_arg)
	glob_list.sort()
	"""
	fctr = 1
        for fname in glob_list:
                #print(fname)
                strval =args.image_dir+"/"+"%(#)06d.jpg" %{"#":fctr}
                #print(strval)
                fctr = fctr + 1
                os.rename(fname,strval)
        glob_list = glob.glob(glob_arg)
        glob_list.sort()
	"""
        try:
		os.remove("img_data.txt")
	except OSError:
		pass
	yolo_file = open("img_data.txt","w")
	img = cv2.imread(glob_list[0])
	height,width,_ = img.shape
	arr = np.zeros((height,width))
	arr_map = np.zeros((height//16,width//16))
	i=0
	for line in glob_list:
		yolo_file.write(line)
		yolo_file.write("\n")
		i=i+1
	yolo_file.close()
	print("[INFO] Image List for YOLO has been created")
	try:
		os.remove("./tools/darknet/img_data.txt")
	except OSError:
		pass
	os.rename("img_data.txt","./tools/darknet/img_data.txt")
	print("[INFO] YOLO will run on all the images. This may take some time...")
	
	with cd("./tools/darknet"):
		if os.name == "nt":
			res = subprocess.Popen(["darknet.exe", "detector", "test", "cfg/coco.data", "cfg/yolov3.cfg", "yolov3.weights","-dont_show", "-ext_output"], stdin=open("img_data.txt","r"), stdout=open("det.txt","w"))
		else:
			res = subprocess.Popen(["./darknet", "detector", "test", "cfg/coco.data", "cfg/yolov3.cfg", "yolov3.weights", "-dont_show", "-ext_output"], stdin=open("img_data.txt","r"), stdout=open("det.txt","w"))
			res.wait()
	
	print("[INFO] Result from YOLO has been generated")
	create_seq_data(i,args.image_dir)
	os.rename("./tools/darknet/det.txt","./tools/deep_sort/tmp/SeqData/det/det.txt")
	
	print("[INFO] We will generate detections file for DeepSORT. Please be patient.")


	with cd("./tools/deep_sort"):
		res1 = subprocess.Popen(["python", "tools/generate_detections.py", "--model=resources/networks/mars-small128.pb", "--mot_dir=./tmp","--output_dir=./resources/detections/custom","--image_dir",args.image_dir])
		res1.wait()
		print("[INFO] DeepSORT detections file is ready... We will now get tracks using DeepSORT...")
		res2 = subprocess.Popen(["python", "deep_sort_app.py", "--sequence_dir=./tmp/SeqData", "--detection_file=./resources/detections/custom/SeqData.npy","--min_confidence=0.3","--nn_budget=100","--display=False","--output_file=track_res.txt", "--image_dir",args.image_dir])
		res2.wait()

	os.rename("./tools/deep_sort/track_res.txt","./track_res.txt")
	
	print("[INFO] Track results have been fetched. Map creation will begin...")
	frame_ids = []
	file = open("track_res.txt","r")
	last_fno = -1
	print('')
	for line in file:
		field = line.split(",")
		#print(int(field[0])," ",int(field[1])," ",float(field[2])," ",float(field[3])," ",float(field[4])," ",float(field[5]))
		if last_fno == -1:
			last_fno = int(field[0])
		fno = int(field[0])
		if fno != last_fno:
			mark_areas(frame_ids,args.motion_thresh,args.lot_thresh)
			last_fno=fno
			frame_ids=[]
		t = TrackID(int(field[0]),int(field[1]),float(field[2]),float(field[3]),float(field[4]),float(field[5]))
		frame_ids.append(t)
	file.close()
	print("[CHECKING] Remaining IDs")
	for j in id_list:
		#print(j.vid," ",j.frame,"v")
		if j.frame > args.lot_thresh:
			add_to_map(j)
			print('')
	map_csv = args.output_file + ".csv"
	map_img = args.output_file + ".jpg"
	np.savetxt(map_csv,arr,delimiter=",")
	mymap = genfromtxt(map_csv,delimiter=",")
	cv2.imwrite(map_img,255*mymap)
	np.savetxt(map_csv,arr_map,delimiter=",")
	#arr6 = mymap.repeat(16, axis=0).repeat(16,axis=1)
