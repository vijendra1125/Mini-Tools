#
# Created on Sat Aug 29 2020
# Author: Vijendra Singh
# License: MIT
# Brief:
#
import os
import cv2
import csv
import numpy as np

import parameters as params


class bb_labeling:
    bb_border_width = 2  # in pixels
    bb_side_min_length = 2  # in pixels

    def __init__(self, label_dict):
        self.label_dict = label_dict
        self.label_key = list(self.label_dict.keys())[0]
        self.label_id = list(self.label_dict.values())[0][0]
        self.label_name = list(self.label_dict.values())[0][1]
        self.bb_color = list(self.label_dict.values())[0][2]
        self.csv_filename = "annotations.csv"

        self.top_left_captured = False
        self.image_labels = []

        if params.START_NEW:
            self.start_new()

    def start_new(self):
        filename = os.path.join(params.OUTPUT_DIR, self.csv_filename)
        if os.path.exists(filename):
            os.remove(filename)
        fields = ['image_name', 'label_key', 'label_name', 'label_id',
                  'bb_id', 'left', 'top', 'right', 'bottom']
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)

    def compile_capture_data(self, left, top, right, bottom):
        return [self.image_name, self.label_key, self.label_name,
                self.label_id, len(self.image_labels),
                left, top, right, bottom]

    def mouse_capture(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            bb_data = self.compile_capture_data(x, y, None, None)
            self.image_labels.append(bb_data)
            self.top_left_captured = True

        elif event == cv2.EVENT_LBUTTONUP:
            left = min(self.image_labels[-1][-4], x)
            top = min(self.image_labels[-1][-3], y)
            right = max(self.image_labels[-1][-4], x)
            bottom = max(self.image_labels[-1][-3], y)
            width_ok = (right-left) > self.bb_side_min_length
            height_ok = (bottom-top) > self.bb_side_min_length
            if (height_ok and width_ok):
                bb_data = self.compile_capture_data(left, top, right, bottom)
                self.image_labels[-1] = bb_data
                cv2.rectangle(self.image,
                              (left, top), (right, bottom),
                              self.bb_color, self.bb_border_width)
                cv2.imshow(self.image_name, self.image)
                self.image_temp = self.image.copy()
            else:
                self.image = self.image_temp.copy()
                del self.image_labels[-1]
            self.top_left_captured = False

        elif self.top_left_captured:
            self.image = self.image_temp.copy()
            left = self.image_labels[-1][-4]
            top = self.image_labels[-1][-3]
            cv2.rectangle(self.image,
                          (left, top), (x, y),
                          self.bb_color, self.bb_border_width)
            cv2.imshow(self.image_name, self.image)

    def read_image(self, name):
        self.image_name = os.path.splitext(name)[0]
        image_path = os.path.join(params.DATA_DIR, name)
        self.image_org = cv2.resize(cv2.imread(image_path), dsize=(0, 0),
                                    fx=params.SCALE_FACTOR, fy=params.SCALE_FACTOR)
        self.image = self.image_org.copy()
        self.image_temp = self.image_org.copy()
        cv2.namedWindow(self.image_name)
        cv2.setMouseCallback(self.image_name, self.mouse_capture)

    def prepare_image(self):
        filename = os.path.join(params.OUTPUT_DIR, self.csv_filename)
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data_list = list(reader)
            header = data_list[0]
            col = len(header)
            row = len(data_list)
            data_array = np.asarray(data_list).reshape(row, col)
            occurence = np.where(data_array[:, 0] == self.image_name)
            self.image_labels = []
            for row in occurence:
                self.image_labels = data_array[row, :].tolist()
        self.bb_count = len(self.image_labels)
        for label in self.image_labels:
            color = self.label_dict[label[1]][2]
            cv2.rectangle(
                self.image, (int(label[-4]), int(label[-3])),
                (int(label[-2]), int(label[-1])),
                color, self.bb_border_width)
        self.image_temp = self.image.copy()

    def write_csv(self):
        filename = os.path.join(params.OUTPUT_DIR, self.csv_filename)
        with open(filename, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.image_labels[self.bb_count:])

    def label_images(self):
        filenames = os.listdir(params.DATA_DIR)
        image_names = []
        for name in filenames:
            if name.endswith(params.FILE_EXT):
                image_names.append(name)
        image_names.sort()
        image_count = len(image_names)
        current_image_id = 0
        while True:
            self.read_image(image_names[current_image_id])
            self.prepare_image()
            while True:
                cv2.imshow(self.image_name, self.image)
                key = cv2.waitKey(1) & 0xFF
                for item in list(self.label_dict.keys()):
                    if key == ord(item):
                        self.label_key = item
                        self.label_id = self.label_dict[item][0]
                        self.label_name = self.label_dict[item][1]
                        self.bb_color = self.label_dict[item][2]
                if key == ord("c"):
                    self.image = self.image_org.copy()
                    del self.image_labels[self.bb_count:]
                elif (key == ord("u")) and (len(self.image_labels) != 0):
                    del self.image_labels[-1]
                    self.image = self.image_org.copy()
                    for label in self.image_labels:
                        color = self.label_dict[label[1]][2]
                        cv2.rectangle(
                            self.image, (int(label[-4]), int(label[-3])),
                            (int(label[-2]), int(label[-1])),
                            color, self.bb_border_width)
                    cv2.imshow(self.image_name, self.image)
                    self.image_temp = self.image.copy()
                elif key == ord("n"):
                    current_image_id = min(current_image_id+1, image_count-1)
                    break
                elif key == ord("p"):
                    current_image_id = max(current_image_id-1, 0)
                    break
                elif key == ord("f"):
                    break
            self.write_csv()
            cv2.destroyWindow(self.image_name)
            if key == ord("f"):
                break
