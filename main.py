import numpy as np
import tracker
from detector import Detector
import cv2
import csv

if __name__ == '__main__':
    # function to write data to a CSV file
    def write_to_csv(type, id, index, timestamp):
        i = index+1
        data = {
            "type": type,
            "id": id,
            "dkh": i,
            "jgsj": timestamp
        }

        filename = "file_name.csv" # can change as you need
        fieldnames = ["type", "id", "dkh", "jgsj"]

        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        print("Data was successfully written to", filename)

    def collision2line(x, y , index, polygon_mask_blue_and_yellow):
        is_collision = False
        try:
            if polygon_mask_blue_and_yellow[y, x] == index+1:
                is_collision = True
        except:
            is_collision = False
        return is_collision

    detection_areas = []
    current_area = []

    def mouse_callback(event, x, y, flags, param):
        global current_area

        if event == cv2.EVENT_LBUTTONDOWN:
            current_area = [(x, y)]

        elif event == cv2.EVENT_LBUTTONUP:
            current_area.append((x, y))
            if len(current_area) == 2:
                x1, y1 = current_area[0]
                x2, y2 = current_area[1]
                top_left = (min(x1, x2), min(y1, y2))
                bottom_right = (max(x1, x2), max(y1, y2))
                top_right = (bottom_right[0], top_left[1])
                bottom_left = (top_left[0], bottom_right[1])

                detection_areas.append([top_left, top_right, bottom_right, bottom_left])
                current_area = []
                print("Detection Area:", detection_areas)

                for area in detection_areas:
                    cv2.rectangle(frame, area[0], area[2], (0, 255, 0), 2)
                cv2.imshow("Frame", frame)

    # open video file
    video_path = "C:/Users/Admin/file_name.mp4" # need to change
    cap = cv2.VideoCapture(video_path)

    # read first frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read the video frame.")
        exit()

    # Create a window and set the mouse callback function
    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", mouse_callback)

    while True:
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    length = len(detection_areas)
############################################################################################
    list_polygon_blue_values = []
    polygon_mask_blue_and_yellow = np.zeros((1080, 1920, 1), dtype=np.uint8)
    for i in range(length):
        mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
        list_pts_blue = detection_areas[i]
        ndarray_pts_blue = np.array(list_pts_blue, np.int32)
        polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=i+1)

        polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]

        list_polygon_blue_values.extend([polygon_blue_value_1.copy()])
        polygon_mask_blue_and_yellow = polygon_mask_blue_and_yellow + polygon_blue_value_1

    # b,g,r
    blue_color_plate = [255, 0, 0]
    # blue polygon picture
    blue_image = np.array(polygon_mask_blue_and_yellow * blue_color_plate, np.uint8)

    # size can be changed
    polygon_mask_blue_and_yellow = cv2.resize(polygon_mask_blue_and_yellow, (1920, 1080))
    color_polygons_image = blue_image
    # size can be changed
    color_polygons_image = cv2.resize(color_polygons_image, (1920, 1080))

    # new dictionary
    new_dic_id = {}
    for i, element in enumerate(list_polygon_blue_values, start=1):
        new_list = []
        new_dic_id[i] = new_list

########################The detection area module ends and enters the video analysis module##########################

    # Initialize yolov5
    detector = Detector()

    # open video
    capture = cv2.VideoCapture("C:/Users/Admin/file_name.mp4") # need to change
    # capture = cv2.VideoCapture('/mnt/datasets/datasets/towncentre/TownCentreXVID.avi')
    video_fps = capture.get(cv2.CAP_PROP_FPS)

    while True:
        # read each frame
        _, im = capture.read()
        if im is None:
            break

        # size can be changed
        im = cv2.resize(im, (1920, 1080))

        list_bboxs = []
        bboxes = detector.detect(im)

        # If there is a bbox in the screen
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)
            output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
            pass
        else:
            # If there is no bbox in the screen
            output_image_frame = im
        pass

        output_image_frame = cv2.add(output_image_frame, color_polygons_image)

        if len(list_bboxs) > 0:
            # ----------------Judgment of hitting the detection area------------------
            for item_bbox in list_bboxs:
                x1, y1, x2, y2, label, track_id = item_bbox
                for index, polygon in enumerate(list_polygon_blue_values):
                    x1_offset = int(x1 + ((x2 - x1) * 0.5))
                    # point of hitting
                    y = y2
                    x = x1_offset
                    a = collision2line(x, y,  index, polygon_mask_blue_and_yellow)
                    if a == True and track_id not in new_dic_id[index+1]:
                        new_dic_id[index+1].append(track_id)
                        jgsj = capture.get(cv2.CAP_PROP_POS_MSEC)
                        print(f'type: {label} | id: {track_id} | 道口号：{index+1} | jgsj: {jgsj}')
                        write_to_csv(label, track_id, index, jgsj)
                    pass
                pass
            pass

        cv2.imshow('demo', output_image_frame)
        cv2.waitKey(1)
        pass
    capture.release()
    cv2.destroyAllWindows()
