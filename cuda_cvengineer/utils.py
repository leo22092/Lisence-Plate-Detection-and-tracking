import easyocr
import string
import re
# initialize ocr reader

reader = easyocr.Reader(['en'], gpu=True)
# from to_excel import log_vehicle_number

# maping dictioneries for charecter conversion
replace_string = [",", ":", ";", ".", " "]
dict_char_to_int = {"O": '0',
                    "I": "1",
                    "J": "3",
                    "A": "4",
                    "G": "6",
                    "S": "5",
                    "Z": "2"}
dict_int_to_char = {'0': "O",
                    "1": "I",
                    "3": "J",
                    "4": "A",
                    "6": "G",
                    "5": "S",
                    "2": "Z"}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                        'license_plate' in results[frame_nmr][car_id].keys() and \
                        'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][
                                                                    0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][
                                                                    1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][
                                                                    2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][
                                                                    3]),
                                                            results[frame_nmr][car_id]['license_plate'][
                                                                'bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate'][
                                                                'text_score'])
                            )
        f.close()


def lisence_complies_format1(text):

    if len(text) <5:
        # print("returned text length is less")

        return False
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys())and \
        (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and\
        (text[2] in ["0","1","2","3","4","5","6","7","8","9"] or text[2] in dict_char_to_int.keys()):
        # (text[3] in ["0", "1", "2", "3", "4", "5", "6","7", "8", "9"] or text[3] in dict_char_to_int.keys())
        # (text[4] is string.ascii_uppercase or text[0] in dict_int_to_char.keys()) or \
        # (text[5] is string.ascii_uppercase or text[0] in dict_int_to_char.keys()) or \
        # (text[-4] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] or text[6] in dict_char_to_int.keys()) and \
        # (text[-3] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] or text[7] in dict_char_to_int.keys()) and \
        # (text[-2] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] or text[8] in dict_char_to_int.keys()) and \
        # (text[-1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] or text[9] in dict_char_to_int.keys()):
        print("returned True from lisence_complies_format")
        return True


def format_lisence1(text):
    print("Format_lisence input = :",text)
    lisence_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int, 6: dict_char_to_int,
               7: dict_char_to_int,
               8: dict_char_to_int,
               9: dict_char_to_int}
    for j in [0, 1, 2, 3, 4, 5, 6 ]:
        if text[j] in mapping[j].keys():
            lisence_plate_ += mapping[j][text[j]]
        else:
            lisence_plate_ += text[j]
    print("Format lisence o/p=: ",lisence_plate_)
    return lisence_plate_
def format_lisence(text):
    print("Format_lisence input = :",text)

    lisence_plate_=""
    for j in range(0,1):
        if text[j] in dict_int_to_char.keys():
            # text[j]=dict_int_to_char[text[j]]
            lisence_plate_+=dict_int_to_char[text[j]]

    for j in range(1,3):
        if text[j] in dict_char_to_int.keys():
            # text[j]=dict_int_to_char[text[j]]
            lisence_plate_+=dict_char_to_int[text[j]]
        else:
            lisence_plate_+=text[j]


    print("Format lisence o/p=: ",lisence_plate_)
    # /changed return value from lisence_plate_ to text

    if len(text)>7:
        return text
    else:
        return None

def lisence_complies_format(text):
    pattern = r"^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{1,4}$"
    return bool(re.match(pattern, text))

def read_lisence_plate(lisence_plate_crop):
    detections = reader.readtext(lisence_plate_crop)
    print("detections", detections)
    print("LEngth of detection is ", len(detections))
    multi_line = ""
    if len(detections) == 2:
        for i in detections:
            bbox, text, score = i
            multi_line += text
            for i in replace_string:
                multi_line = multi_line.upper().replace(i, "")
        print("multi_line text is ", multi_line)
        if lisence_complies_format(multi_line):
            print("old 2 line text is lisence_late_complies_format ret ", multi_line)

            multi_line_text=format_lisence(multi_line)
            print("New 2 line text is lisence_late_complies_format ret ", multi_line)
            return multi_line_text, score
        else:
            print("NOT COMPLYING FORMAT")
            return None, None
    else:
        for detection in detections:
            bbox, text, score = detection
            text = text.upper().replace(" ", "")
            print(text)
            print("for again")
            if lisence_complies_format(text):
                return text, score

        return None, None


def get_car(lisence_plate, vehicle_track_ids):
    # takes in coordinates of lisence plate list of vehicletrack ids and their coordintes
    x1, y1, x2, y2, score, class_id = lisence_plate
    foundIt = False
    for j in range(len(vehicle_track_ids)):
        # iterating over all the bounding boxs of car
        xcar1, ycar1, xcar2, ycar2, class_id = vehicle_track_ids[j]
        # and verify if it contains lisence plate
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_index = j
            foundIt = True
            break

    if foundIt:
        print("Car id is ..",vehicle_track_ids[car_index])
        return vehicle_track_ids[car_index]

    return -1, -1, -1, -1, -1
