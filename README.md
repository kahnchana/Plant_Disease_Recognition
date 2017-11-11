# Plant_Disease_Recognition
Raspberry Pi based system to detect and recognize plant diseases. Protoype device below:
https://youtu.be/SQslmbeOhpQ

## Dependencies
* Raspberry Pi 3
* Raspberry Pi Camera
* Raspberry Pi NoIR Camera
* Python 2.7
* Tensorflow Library
* OpenCV Python Library
* Tkinter Library


## Recognition Phase

This phase focuses on recognizing an exact plant disease when an image of a particular plant is input to the system. Our project focuses on tomato plants and 7 key diseases common among these plants for the purpose of this research. 

To run the regonition part based on a CNN execute:
python label_image.py test/name_of_image_to_test.jpg 

Required data for this file to run is hosted on drive (excessive size):
https://goo.gl/z5kDFg


Contents of link should be placed within a folder named tf_files. The code above (label_image.py) should be run from within tf_files. 
The system outputs a probability of the image belonging to each class (healthy and 7 diseases). 

The file to be run on the raspberry pi is main.py. This is configured to run at startup in our system. 

## Detection Phase

The detection phase makes use of an RGB and NIR video feed to compute NDVI index for plant images. This will be used to detect infected regions in plant fields / greenhouses. 

More to be added. 


## Acknowledgement

We are thankful for PlantVillage organization for providing us access to plant disease image databases.
We also appreciate the support by Plant Virus Indexing Centre, Homagama.
