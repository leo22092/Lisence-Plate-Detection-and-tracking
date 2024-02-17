from constants import *
import cv2
from datetime import datetime
import os
class Camera:
    def __init__(self):

        pass
    def video_stream(cam_no):
        vid = cv2.VideoCapture(cam_no)
        while True:
            ret, frame = vid.read()
            if ret:
                # cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                yield frame

# {
# for frame in video_stream(cam1):
    # cv2.imshow('Display', frame)
# }
def image_saving(img_roi):
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    print(os.listdir())
    if 'plates' not in os.listdir():
        os.mkdir('plates')
    cv2.imwrite("plates/scaned_img_" + str(count) + "_" + str(current_time) + ".jpg", img_roi)


def processing(frame):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray",frame)
    harcascade = "haarcascade_russian_plate_number.xml"
    plate_cascade=cv2.CascadeClassifier(harcascade)
    plates=plate_cascade.detectMultiScale(gray,1.1,4)
    #     4->no of neighbouring rectangles to confirm
    #      1.1->smaller value more accurate detection
    print(plates)
    for x,y,w,h in plates:
        area=w*h
        if area>min_area:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),5)
            cv2.imshow("gray",frame)
            img_roi = gray[y: y + h, x:x + w]
            # image_saving()
            if cv2.waitKey(1) & 0xFF == ord('s'):
                image_saving(img_roi)



for frame in Camera.video_stream(cam1):
    processing(frame)

# vid.release()
# cv2.destroyAllWindows()


