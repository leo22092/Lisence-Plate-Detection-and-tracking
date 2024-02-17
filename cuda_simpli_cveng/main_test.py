import os
import time
import cv2
import easyocr
# from ultralytics import YOLO
# import pandas

# lisence_platedetector=YOLO("C:\\Users\\shitosu\\Desktop\\v8\\best.pt")

# coco_model=YOLO('yolov8n.pt')

cap=cv2.VideoCapture(0)

reader=easyocr.Reader(['en'],gpu=True)

# print(os.walk('images'))
frame_no=0
while True:
    frame_no+=1
    if frame_no%2==0:
        cv2.imshow("ghj",frame)

        pass
    else:
        print("FRame no",frame_no)
        ret,frame=cap.read()
        # detections=lisence_platedetector(frame)[0]
        # for detection in detections.boxes.data.tolist():
        #     x1,y1,x2,y2,score,class_id=detection
        #     cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,255),2)
        #     result = reader.readtext(frame)
        #     if len(result)!=0:
        #         cv2.putText(frame,str(result[0]),(int(x1),int(y1)),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)

        cv2.imshow("ghj",frame)
        # img=cv2.imread(f)
        # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        start=time.time()
        result=reader.readtext(frame)
        end=time.time()
        print("Elapsed time ",end-start)
        print(result)
        cv2.waitKey(1)
# for i in os.listdir('images'):
#     f=os.path.join('images',i)
#     img=cv2.imread(f)
#     start=time.time()
#     result=reader.readtext(img)
#     end=time.time()
#     print("Elapsed time ",end-start)
#     print(result)
