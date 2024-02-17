from multiprocessing import Process
from webcam2 import Camera
from constants import *

camera1=Camera(cam1)
camera2=Camera(cam2)
def run_script1(test):
    # Run script1
    for frame in camera1.video_stream():
        camera1.processing(frame)
def run_script2():
    # Run script2
    for frame in camera2.video_stream():
        camera2.processing(frame)
if __name__ == '__main__':
    # Create two processes for each script
    p1 = Process(target=run_script1)
    p2 = Process(target=run_script2)

    # Start both processes
    p1.start()
    p2.start()