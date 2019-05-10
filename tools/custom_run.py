import subprocess

res1 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/A", "--output_file=pu_sun_A_30","--lot_thresh=30"])
res1.wait()

res2 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/B", "--output_file=pu_sun_B_30","--lot_thresh=30"])
res2.wait()

res3 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/C", "--output_file=pu_sun_C_30","--lot_thresh=30"])
res3.wait()

res4 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/D", "--output_file=pu_sun_D_30","--lot_thresh=30"])
res4.wait()

res5 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/E", "--output_file=pu_sun_E_30","--lot_thresh=30"])
res5.wait()

res6 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/F", "--output_file=pu_sun_F_30","--lot_thresh=30"])
res6.wait()

res7 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/G", "--output_file=pu_sun_G_30","--lot_thresh=30"])
res7.wait()

res8 = subprocess.Popen(["python", "park_map_app.py", "--image_dir=/media/harddisk/Nikhil/datasets/PKLot/PKLot/PUCPR/Sunny/H", "--output_file=pu_sun_H_30","--lot_thresh=30"])
res8.wait()
