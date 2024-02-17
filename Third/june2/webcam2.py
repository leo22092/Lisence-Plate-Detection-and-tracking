from constants import *
import constants
import cv2
from datetime import datetime
import os
import sys


from logger import logging
from exception import CustomException



class Camera:
    def __init__(self,cam_no):
        self.cam_no=cam_no
    def video_stream(self):
        vid = cv2.VideoCapture(self.cam_no)
        while True:
            ret, frame = vid.read()
            if ret:
                # cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logging.info("Exiting on pressing q")
                    vid.release()
                    cv2.destroyAllWindows()
                    break

                yield frame
    # def release(self):
    #     self.release()
    #     cv2.destroyAllWindows()

# {
# for frame in video_stream(cam1):
    # cv2.imshow('Display', frame)
# }
    def image_saving(self,img_roi):

        now = datetime.now()
        current_time = now.strftime("%H_%M_%S")
        # print(os.listdir())
        cam_name=str(self.cam_no)
        if 'plates_camera_'+cam_name not in os.listdir():
            os.mkdir('plates_camera_'+cam_name)
        cv2.imwrite(f"plates_camera_{cam_name}/cap_img_{str(constants.count)}_{str(current_time)}.jpg", img_roi)
        logging.info(f"saving plate image in -->plates_camera_{cam_name} as cap_img_{str(constants.count)}_{str(current_time)}.jpg")

        constants.count+=1



    def processing(self,frame):
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray",frame)
        harcascade = "sources\haarcascade_russian_plate_number.xml"
        plate_cascade=cv2.CascadeClassifier(harcascade)
        plates=plate_cascade.detectMultiScale(gray,1.1,4)
        #     4->no of neighbouring rectangles to confirm
        #      1.1->smaller value more accurate detection
        print(plates)
        for x,y,w,h in plates:
            area=w*h
            if area>min_area:
                logging.info("Area > min area")
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),5)
                cv2.imshow("gray",frame)
                img_roi = gray[y: y + h, x:x + w]
                # image_saving()
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    self.image_saving(img_roi)


if __name__=='__main__':

    camera1=Camera(cam1)
    # camera2=Camera(cam2)
    for frame in camera1.video_stream():
        try:
            camera1.processing(frame)
        except Exception as e:
            logging.info("Camera2 processing error")
            raise CustomException(e, sys)

# vid.release()
# cv2.destroyAllWindows()


