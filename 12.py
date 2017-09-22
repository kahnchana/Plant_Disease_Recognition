#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 04 08:34:17 2017

@author: Hiran
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 15:51:49 2017

@author: Hiran
"""
def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]
clear_all()

import imutils
from imutils.video import VideoStream
import cv2
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import time
import os
import sys
import tensorflow as tf

stopEvent = threading.Event()
pause_=False
stop_=False
outputPath="/home/pi/Documents/RaspChallenge"
root=tk.Tk()
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
print root.winfo_screenwidth(),root.winfo_screenheight()

#video=VideoStream(usePiCamera=True,resolution=(640,480)).start()
#video.set(3,1024)
#video.set(4,720)
time.sleep(0.2)

def videoLoop():
		global panel
		global frame
		while (not stop_):       	    
					try:
			# keep looping over frames until we are instructed to stop
						while not stopEvent.is_set() and not stop_ :
				# grab the frame from the video stream 
							frame = video.read()
														                
							#if not ret:continue
              # OpenCV represents images in BGR order; however PIL
				# represents images in RGB order, so we need to swap
				# the channels, then convert to PIL and ImageTk format
				#cv2.imshow(frame)            
							image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
							image = Image.fromarray(image)
							image = image.resize((320, 240),Image.ANTIALIAS)
							image = ImageTk.PhotoImage(image)
		
				# if the panel is not None, we need to initialize it
							if panel is None:
								panel = tk.Label(image=image)
								panel.image = image
					#panel.pack(side="top", padx=10, pady=10)
								panel.grid(row=1,column=2,columnspan=2,rowspan=3,sticky=tk.W+tk.E+tk.N+tk.S)
		
				# otherwise, simply update the panel
							else:
								panel.configure(image=image)
								panel.image = image
						while pause_ and not stop_:                                                    
							if panel is None:
								panel = tk.Label(image=image)
								panel.image = image
					#panel.pack(side="top", padx=10, pady=10)
								panel.grid(row=1,column=2,columnspan=2,rowspan=3,sticky=tk.W+tk.E+tk.N+tk.S)
		
				# otherwise, simply update the panel
							else:
								panel.configure(image=image)
								panel.image = image                
 
					except RuntimeError,e:                                             
						pass

					        

def takePic():
		# grab the current timestamp and use it to construct the
		# output path
		ts = datetime.datetime.now()
		filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		p = os.path.sep.join((outputPath, filename))
 
		# save the file
		cv2.imwrite(p, frame.copy())
		txt.delete(1.0, tk.END)
		txt.insert(tk.END,"[INFO] saved {}".format(filename)+"\n")
		
		#recognition code
		image_path = filename
		image_data = tf.gfile.FastGFile(image_path, 'rb').read()
		label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("retrained_labels.txt")]
				   
		# Unpersists graph from file
		with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
			graph_def = tf.GraphDef()
			graph_def.ParseFromString(f.read())
			tf.import_graph_def(graph_def, name='')				   
		
		with tf.Session() as sess:
			# Feed the image_data as input to the graph and get first prediction
			softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
			
			predictions = sess.run(softmax_tensor, \
					 {'DecodeJpeg/contents:0': image_data})
			
			# Sort to show labels of first prediction in order of confidence
			top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
			
			for node_id in top_k:
				human_string = label_lines[node_id]
				score = predictions[0][node_id]
				txt.insert(tk.END,'%s (score = %.5f)' % (human_string, score) + "\n")
        

def stop():
    # set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		global stop_
		stop_=True
		print("[INFO] closing...")
		stopEvent.set()
		video.stop()
		root.quit()
		root.destroy()
	        os._exit(0)

		



def play():
    
    global pause_
    stopEvent.clear()
    pause_=False
    btn3.grid_remove()
    btn1.grid()
    txt.delete(1.0,tk.END)
    txt.insert(tk.END,"Welcome\nto the\nTreeDoc\n\n\n\nPlease place\na specimen\nunder the\nimage sensor\nand click\n  START!!!\n")

    
    
def pause():

    global pause_
    pause_=True
    stopEvent.set()
    btn1.grid_remove()
    btn3.grid()
    
    


def multifunction(*args):
    for function in args:
        function()



frame = None
thread = None
panel=None



#buttons
btn1 = tk.Button(root, text="Start", command=lambda: multifunction(takePic, pause),height=2,width=7)
#btn1.pack(side="bottom", padx=5,pady=5)
btn2 = tk.Button(root, text="Quit",command=stop,height=2,width=7)
btn3=tk.Button(root,text="Continue",command=play,height=2,width=7)
#btn2.pack(side="bottom",padx=5,pady=5)
btn1.grid(row=1,column=0,rowspan=1,columnspan=1,sticky=tk.W+tk.E+tk.N+tk.S)
btn2.grid(row=4,column=0,rowspan=1,columnspan=1,sticky=tk.W+tk.E+tk.N+tk.S)
btn3.grid(row=1,column=0,rowspan=1,columnspan=1,sticky=tk.W+tk.E+tk.N+tk.S)
btn3.grid_remove()
txt=tk.Text(root,height=20,width=30)
txt.grid(row=1,column=7,rowspan=6,columnspan=3,sticky=tk.W+tk.E+tk.N+tk.S)
txt.insert(tk.END,"Welcome\nto the\nTreeDoc\n\n\n\nPlease place a \nspecimen under \nthe image sensor\nand click start\n")

#video stream
thread = threading.Thread(target=videoLoop, args=())
thread.start()

root.wm_title("TreeDoc")
root.mainloop()
