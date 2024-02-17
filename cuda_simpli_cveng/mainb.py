import numpy as np
from ultralytics import YOLO
import cv2
import utils

vid_path="C:\\Users\shitosu\Desktop\Tkm_front.mp4"
model_path="C:\\Users\\shitosu\\Desktop\\v8\\best.pt"

license_plate_detector_model = YOLO(model_path)
cap=cv2.VideoCapture(vid_path)

while cap.isOpened():
    ret, frame = cap.read()
    frame_no=0
    if ret:
        frame_no+=1
        if frame_no%100==0:
            input_csv_file = "output.csv"
            output_csv_file = "sorted_out.csv"
            utils.process_csv(input_csv_file, output_csv_file)
        license_plates = license_plate_detector_model(frame)[0]
        detections=[]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
            x1=int(x1)
            y1=int(y1)
            x2=int(x2)
            y2=int(y2)
            score=int(score)

            license_plate_crop = frame[y1:y2, x1:x2]
            cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 0, 255), 2)
            license_plate_text, license_plate_text_score = utils.read_license_plate(license_plate_crop)
            if (license_plate_text,license_plate_text_score)!=(None,None) and len(license_plate_text)>=7:
                if license_plate_text_score >=0.3:
                    if utils.license_complies_format(license_plate_text) :
                        utils.write_text_to_csv(license_plate_text,license_plate_text_score,'output.csv')
                        cv2.putText(frame, license_plate_text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

                print(license_plate_text)
                # cv2.putText(frame, license_plate_text, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
        cv2.imshow("plate", frame)

        cv2.waitKey(1)
    else:
        print("stoppping")
        break