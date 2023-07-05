'''
Band Edge Thermometry Reader

Paromita Mitchell 07/05/2023
@paroperha

This program takes in data from two cameras to determine transition points of opacity.
This will allow us to determine set points of temperature behavior.
It also serves as a demonstration of temperature dependence of the Band Edge.

There are a few stages to this:
1. Read from two cameras (temperature reading from hotplate, and wafer)
    a) Average the wafers frames.
    b) Save both the temperature and the wafer measurement with filename time.
2. Live feed.
3. Read temperature from picture, or from external temperature sensor.
4. Threshold check for brightness (compare brightness of two points)
5. Edge detect to determine wafer image visibility as a comparison

'''

'''
STAGE 1:
Read from two cameras and keep track of times. This will allow me to make a video
or some such putting this data together. I can manually put the data into a graph.
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

from imutils.video import VideoStream   # Faster image grabbing threading.

# Read from the cameras using VideoStream. 
def stream_init(source):
    return VideoStream(src=source).start()

# Init two cameras
def stream_init_all(srct, srcsc):
    vst = stream_init(srct)
    vssc = stream_init(srcsc)
    return vst, vssc

# Read from a camera
# TODO Check if the frame is good
def read_frame(vs):
    return vs.read()

def read_frames(vst, vssc):
    return read_frame(vst), read_frame(vssc)

# Output the average of one of the cameras every some amount of time.
def average_frames(vssc):
    pass

# Display both cameras side by side when function run.
def display_images(temp_frame, sc_frame):
    cv2.imshow('Temp Frame', temp_frame)
    cv2.imshow('Semiconductor Frame', sc_frame)

# Format time
def format_time(t):
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(t))


# Save them into a folder
def save_images(test_name, temp_frame, semi_frame):
    strtime = format_time(time.time())
    prefix = folder_name + test_name + "_" + strtime
    print(folder_name + test_name + "_" + strtime + "_t" + file_ext)
    
    save_image(prefix + "-t" + file_ext, temp_frame)
    save_image(prefix + "-sc" + file_ext, semi_frame)
       
def save_image(name, frame):
    if not cv2.imwrite(name, frame):
        raise Exception("Could not write image: ", name)

# Check for quit
def check_quit():
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    return key == ord("q")


# Quit all things safely
def close_all(vst, vssc):
    cv2.destroyAllWindows()

    # TODO Check for all capture and vs
    vst.stop()
    vssc.stop()



#############################################

srct = 0
srcsc = 1
folder_name = "images/"
file_ext = ".jpg"
test_name = "E1"
save_rate = 1     # seconds before next save


vst, vssc = stream_init_all(srct, srcsc)

done = False
t = ts = time.time()    # t is tracking time, ts is every time image saved.
tdiff = 0

# Check time, read both frames, display them.
while not done:
    # Measure time elapsed
    t = time.time()
    print("Time is:", format_time(t))

    # Read and display frames
    temp_frame, sc_frame = read_frames(vst, vssc)

    display_images(temp_frame, sc_frame)

    # Don't need to save all frames, can do every few:
    print(t - ts)
    if t - ts >= save_rate:
        print("Saving image")
        save_images(test_name, temp_frame, sc_frame)
        ts = t

    done = check_quit()

# Close everything

close_all(vst, vssc)