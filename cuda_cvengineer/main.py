import numpy as np
from ultralytics import YOLO
import cv2

import utils
from sort.sort import *
from utils import *
# from  to_excel import log_vehicle_number

results={}
mot_tracker=Sort()
# load mode
coco_model=YOLO('yolov8n.pt')
lisence_plate_detector = YOLO("C:\\Users\\shitosu\\Desktop\\v8\\best.pt")
# load video
# cap=cv2.VideoCapture("C:\\Users\\shitosu\Desktop\\Mini_project\\Dataset_collected\\noplatevidio\medicalclg_vid.mp4")
cap=cv2.VideoCapture('cuttkm_frnt.mp4')
# cap=cv2.VideoCapture('cut2.mp4')


# cap=cv2.VideoCapture(0)
# read frames
ret= True
frame_no= -1
vehicles=[2,3,5,7]
while ret:
    frame_no += 1
    print("Frame no .",frame_no)
    ret,frame=cap.read()
    results[frame_no] = {}

    if ret and frame_no<=900:
        # cv2.imshow("sss",frame)



        # detect vehicles
        detections = coco_model(frame)[0]
        detections_ = []

        for detection in detections.boxes.data.tolist():
            x1,y1,x2,y2,score,class_id=detection

            if int(class_id) in vehicles:
                detections_.append([x1,y1,x2,y2,score])
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

        # track vehicles
        track_ids=mot_tracker.update(np.asarray(detections_))
        cv2.imshow("plate", frame)

        # dect lisence plates
        lisence_plates=lisence_plate_detector(frame)[0]
        for lisence_plate in lisence_plates.boxes.data.tolist():
            x1,y1,x2,y2,score,class_id=lisence_plate
            cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),2)
            cv2.imshow("plate",frame)


            # assign lisence plate to vehicle
            xcar1,ycar1,xcar2,ycar2,car_id=get_car(lisence_plate,track_ids)
            if car_id!= -1:

                # crop lisemce plate
                lisence_plate_crop=frame[int(y1):int(y2),int(x1):int(x2)]

                # process lisence plate
                lisence_plate_crop_gray=cv2.cvtColor(lisence_plate_crop,cv2.COLOR_BGR2GRAY)
                lisence_plate_gray = cv2.cvtColor(lisence_plate_crop, cv2.COLOR_BGR2GRAY)
                lisence_plate_thresh = cv2.adaptiveThreshold(lisence_plate_gray,
                                                             255,
                                                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                             cv2.THRESH_BINARY,
                                                             31,
                                                             10)
                cv2.imshow("Thresholded",lisence_plate_thresh)
                # read lisence plate number
                lisence_plate_text,lisence_plate_text_score=utils.read_lisence_plate(lisence_plate_crop)
                print("From main function :",lisence_plate_text)
                # write results
                cv2.putText(frame, lisence_plate_text, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

                if lisence_plate_text is not None and lisence_plate_text_score>=0.60:
                    cv2.imshow("plate", frame)
 
                    # results[frame_no][class_id]={'car':{'bbox':[xcar1,ycar1,xcar2,ycar2]},
                    #                             "Lisence_plate":{'bbox':[x1,y1,x2,y2],
                    #                                      'text':lisence_plate_text,
                    #                                      'bbox_score':score,
                    #                                      'text_score':lisence_plate_score}}
                    results[frame_no][class_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                  'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': lisence_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': lisence_plate_text_score}}
        cv2.waitKey(1)

write_csv(results,'./test.csv')