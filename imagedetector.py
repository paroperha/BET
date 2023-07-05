import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

from imutils.video import VideoStream
from xlsxwriter import Workbook

fig = plt.figure()

plt.ion()  # Set interactive mode on

seconds_fudge = 5
xs = []
blue = []
red = []
green = []

b_frame = []
g_frame = []
r_frame = []
s_frame = []

#Note to self: currently fixing the timing issue with videostream going way too fast.

def find_fps():
    # Start default camera
    # video = cv2.VideoCapture(0)
 
    # # Find OpenCV version
    # (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
    # # With webcam get(CV_CAP_PROP_FPS) does not work.
    # # Let's see for ourselves.
 
    # if int(major_ver)  < 3 :
    #     fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    #     print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    # else :
    #     fps = video.get(cv2.CAP_PROP_FPS)
    #     print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
 
    # Number of frames to capture
    num_frames = 12000

    vs = VideoStream().start()
 
    print("Capturing {0} frames".format(num_frames))
 
    # Start time
    start = time.time()
    frame = None
 
    # Grab a few frames
    for i in range(0, num_frames) :
        while frame is None:
            frame = vs.read()

        
 
    # End time
    end = time.time()
 
    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))
 
    # Calculate frames per second
    fps  = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))
 
    vs.stop()

    return fps

# We will be using Video-capture to get the fps value.
capture = cv2.VideoCapture(0)
fps = capture.get(cv2.CAP_PROP_FPS)
print(fps)
capture.release()

#or not.
fps = 30

# New module: VideoStream
vs = VideoStream().start()

frame_count = 0
second = 1

is_new_frame = False
start_time=0
frame = np.array([0])

while True:
    
    print(time.time() - start_time)
    start_time = time.time()

    frame = vs.read()

    if frame is None:
        print("Done")
        break

    print(frame_count, frame_count % int(fps))
    if frame_count % int(fps) == 0:
        print("updating")
        b, g, r = cv2.split(frame)

        is_new_frame = True  # New frame has come

        # Check lines match up
        line = [line for line in zip(b, g, r) if len(line)]

        b, g, r = zip( * line)

        s_frame.append(second)
        b_frame.append(np.mean(b))
        g_frame.append(np.mean(g))
        r_frame.append(np.mean(r))


        plt.plot(s_frame, b_frame, 'b', label='blue', lw=7)
        plt.plot(s_frame, g_frame, 'g', label='green', lw=4)
        plt.plot(s_frame, r_frame, 'r', label='red')
        plt.xlabel('seconds')
        plt.ylabel('mean')
        if frame_count == 0:
            plt.legend()

        plt.show()

        plt.pause(1)
        second += 1

    elif second > 2:
        if is_new_frame:

            if second == 3:
                blue.extend(b_frame)
                green.extend(g_frame)
                red.extend(r_frame)
                xs.extend(s_frame)
            else:
                blue.append(b_frame[len(b_frame)-1])
                green.append(g_frame[len(g_frame)-1])
                red.append(r_frame[len(r_frame)-1])
                xs.append(s_frame[len(s_frame)-1])

            del b_frame[0]
            del g_frame[0]
            del r_frame[0]
            del s_frame[0]

            is_new_frame = False  # we added the new frame to our list structure

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cv2.destroyAllWindows()
capture.release()
vs.stop()

book = Workbook('Channel.xlsx')
sheet = book.add_worksheet()

row = 0
col = 0

sheet.write(row, col, 'Seconds')
sheet.write(row + 1, col, 'Blue mean')
sheet.write(row + 2, col, 'Green mean')
sheet.write(row + 3, col, 'Red mean')

col += 1

for s, b, g, r in zip(xs, blue, green, red):
    sheet.write(row, col, s)
    sheet.write(row + 1, col, b)
    sheet.write(row + 2, col, g)
    sheet.write(row + 3, col, r)
    col += 1

book.close()