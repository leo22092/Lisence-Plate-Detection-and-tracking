import cv2
import numpy as np
cap=cv2.VideoCapture('veh2.mp4')
cap.set(3,480)
cap.set(4,640)
_,frame1=cap.read()
_,frame2=cap.read()


while cap.isOpened():

    diff=cv2.absdiff(frame1,frame2)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur =cv2.GaussianBlur(gray,(5,5),0)
    _,thresh=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated=cv2.dilate(thresh,None,iterations=2)
    contours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1,contours,-1,(0,255,0),2)

    for cnt in contours:
        (x,y,w,h)=cv2.boundingRect(cnt)
        if cv2.contourArea(cnt)<1000:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,0,255),2)

        cv2.putText(frame1,"status movement ",(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    if __name__=="__main__":
        cv2.imshow("feed",frame1)
        frame1=frame2
        ret,frame2=cap.read()
        cv2.namedWindow("diff", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("diff", 900, 1200)
        cv2.imshow("diff",dilated)
        if cv2.waitKey(40) == 27:
            break

