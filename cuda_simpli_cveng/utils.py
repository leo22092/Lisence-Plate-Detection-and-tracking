import easyocr
import string
import cv2
# import datetime
from datetime import datetime,timedelta
import re
import csv
import difflib
reader = easyocr.Reader(['en'], gpu=True)
replace_string = [",", ":", ";", ".", " ","(",")"]

def read_license_plate(liscense_plate_crop):
    # print("enterendreadliscense")
    detections = reader.readtext(liscense_plate_crop)
    multi_line = ""
    if len(detections)==3:
        for i in detections:
            # print("Detectio len 2b")
            bbox, text, score = i
            multi_line += text
            for i in replace_string:
                multi_line = multi_line.upper().replace(i, "")
        multi_line = multi_line.replace('IND', "")

        return multi_line,score




    if len(detections) == 2:
        # print("Detectio len 2")
        for i in detections:
            # print("Detectio len 2b")
            bbox, text, score = i
            multi_line += text
            for i in replace_string:
                multi_line = multi_line.upper().replace(i, "")
        return multi_line,score
    elif len(detections)==1:
        # print("Detectio len 1a")
        for detection in detections:
            # print("Detectio len 1b")
            bbox, text, score = detection
            text = text.upper().replace(" ", "")
            return text, score
    else:
        return None,None
def liscense_complies_format(text):
    pattern = r"^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{1,4}$"
    return bool(re.match(pattern, text))

def write_text_to_csv(text,confidence, file_name):
    data_dict={}
    try:
        current_datetime = datetime.now()
        date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # data_dict[date_time_str] = text
        data_dict[date_time_str] = {'text': text, 'confidence': confidence}

        with open(file_name, 'a') as csv_file:
            # csv_file.write(text+'\n')
            csv_file.write(f"{date_time_str},{text},{confidence}\n")

        print(f"Text '{text}' written to '{file_name}' successfully.")
    except Exception as e:
        print(f"Error: {e}")


def is_similar(row1, row2, threshold=6):
    text1 = row1[1]  # Assuming the text is in the second column
    text2 = row2[1]
    diff_count = list(difflib.ndiff(text1, text2)).count(' ')
    return diff_count <= threshold




def process_csv(input_file, output_file, similarity_threshold=4):
    try:
        data_dict = {}
        with open(input_file, 'r') as input_csv:
            reader = csv.reader(input_csv)
            next(reader)  # Skip the header row

            current_time = None
            current_vehicles = []

            for row in reader:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                vehicle = row[1]
                confidence = float(row[2])

                if current_time is None:
                    current_time = timestamp
                elif timestamp - current_time > timedelta(seconds=10):
                    process_and_store(current_time, current_vehicles, data_dict, similarity_threshold)
                    current_vehicles = []
                    current_time = timestamp

                current_vehicles.append((vehicle, confidence))

            # Process any remaining vehicles
            if current_vehicles:
                process_and_store(current_time, current_vehicles, data_dict, similarity_threshold)

        # Write processed data to output file
        with open(output_file, 'w', newline='') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(["Date and Time", "Vehicle Number", "Max Confidence"])
            for key, info in data_dict.items():
                writer.writerow([key, info['vehicle'], info['max_confidence']])

        print(f"Processed '{input_file}' and stored results in '{output_file}' successfully.")
    except Exception as e:
        print(f"Error: {e}")


def process_and_store(timestamp, vehicles, data_dict, similarity_threshold):
    vehicle_counts = {}
    for vehicle, confidence in vehicles:
        if vehicle in vehicle_counts:
            vehicle_counts[vehicle].append(confidence)
        else:
            vehicle_counts[vehicle] = [confidence]

    for vehicle, confidences in vehicle_counts.items():
        max_confidence = max(confidences)
        key = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if key not in data_dict:
            data_dict[key] = {'vehicle': vehicle, 'max_confidence': max_confidence}
        else:
            if max_confidence > data_dict[key]['max_confidence']:
                data_dict[key]['max_confidence'] = max_confidence
