# Parking Framework for Unstructured Parking

## Introduction

The system is developed to manage spaces where parking lots are not well defined. In India and some other countries, often the sides of a street are used for parking vehicles even though they may not be dedicated for parking which causes a delay at the intersection. In this scenario, a smart parking system will help mitigate the traffic congestion issues by suggesting the locations available for parking. The system needs to estimate the regions that are used for parking in a given scene by looking at the historical data in the context of a camera. This estimated parking lot map can then be used to infer the number of empty parking lots in the field of view of an edge device.

## Dependencies

All the dependencies for running this system are listed in the requirements.txt file. YOLO is used for detections and DeepSORT is used for tracking vehicles. They are listed in tools folder. YOLO pretrained weights must be downloaded in the darknet folder before executing the main script. This can be carried out with the following commands:
```
wget  https://pjreddie.com/media/files/yolov3.weights
```
Once download is complete, YOLO must be compiled to create an executable. CUDA and OPENCV flags in the Makefile can be modified inside tools/darknet folder as per the system configuration. All of this will be automatically done by a setup.py file which will be added to the repository soon. The commands to do it manually are:
```
~/parking_framework> cd tools/darknet
~/parking_framework/tools/darknet> make
```

## Running the Map Creator

This is used to get proposals for probable parking spaces. The Map Creator requires historical data provided in the form of a set of images which should be named using a string of 6 characters representing the frame number. For example, the first frame should be named 000001.jpg and the second frame as 000002.jpg and so on. This can be automatically done by the script if the comment is removed from lines [219-227] in park_map_app.py. To see the parameters required by park_map_app.py use the following command:
```
~/parking_framework> python park_map_app.py -h
```
This will display a list of possible flags that can be provided. The complete path to the source image directory must be provided and the output file name must only be a string without extensions. The program will generate three output files: a .csv, a .jpg and .info file which will be useful for making inferences. The Lot Threshold value is the threshold which specifies how many frames a vehicle should be traced for before marking it as a parked vehicle. This varies with the capture frequency of the frames provided in the source image directory. If the images have been taken at intervals of 2 minutes each, a lot threshold of 10 would mean all possible places where a car has been parked for 20 or more minutes.

## Provided Tools

### Custom Run
This is the tools/custom_run.py script which can be used to run the park_map_app.py script on a set of image directories rather than a single directory.

### Video Frames
In case there is a video on which the script is to be run, tools/vidframe.py can be used to generate image frames from a given video. 

### SORT Map
This is the tools/sorted_map.py script which can be used with an alternate object detector. The detections file has to be placed in the Sequence Data folder of DeepSORT in order to use this script. It helps in plugging in different detectors and experimenting with them inside the proposed framework. 

### Weighted Average
This is the tools/wavg.py script and it can be used to super-impose the created map on a sample image from the dataset to visualize the created map.
