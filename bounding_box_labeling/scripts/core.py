#
# Created on Sat Aug 29 2020
# Author: Vijendra Singh
# License: MIT
# Brief:
#
import cv2
import os
import csv

import parameters as params


class bb_labeling:
    def __init__(self, name):
        self.name = name
        self.captured_bb = []
        self.top_left_captured = False
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.capture_bb)
        self.image_labeled = False

    def read_image(self, image_path):
        self.image_org = cv2.imread(image_path)
        self.image_org = cv2.resize(self.image_org, dsize=(0, 0),
                                    fx=params.SCALE_FACTOR, fy=params.SCALE_FACTOR)
        self.image = self.image_org.copy()
        self.image_temp = self.image_org.copy()
        self.image_previous = self.image_org.copy()

    def capture_bb(self, event, x, y, flags, param):
        self.image_temp = self.image.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            self.captured_bb.append((x-1, y-1))
            self.top_left_captured = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.captured_bb.append((x, y))
            cv2.rectangle(self.image_temp,
                          self.captured_bb[-2], self.captured_bb[-1],
                          (0, 255, 0), 2)
            cv2.imshow("image", self.image_temp)
            self.top_left_captured = False
            self.image_previous = self.image.copy()
            self.image = self.image_temp.copy()
        elif self.top_left_captured:
            cv2.rectangle(self.image_temp,
                          self.captured_bb[-1], (x, y), (0, 255, 0), 2)
            cv2.imshow("image", self.image_temp)

    def find_bb_center(self):
        self.bb_centers = []
        for node_id, i in enumerate(range(0, len(self.captured_bb), 2)):
            print(self.captured_bb[i], self.captured_bb[i+1])
            x1, y1 = self.captured_bb[i]
            x2, y2 = self.captured_bb[i+1]
            node_x = min(x1, x2) + abs(x1-x2)//2
            node_y = min(y1, y2) + abs(y1-y2)//2
            self.bb_centers.append([node_id, (node_x, node_y),
                                    self.captured_bb[i], self.captured_bb[i+1]])
            print(self.bb_centers[node_id][1], node_id)

    def save_labeled_images(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        for i in range(len(self.bb_centers)):
            cv2.circle(self.image_org,
                       self.bb_centers[i][1], 2, (0, 255, 0), -1)
            cv2.putText(self.image_org, str(
                self.bb_centers[i][0]), self.bb_centers[i][1], font, font_scale, (0, 0, 255), 2)
        cv2.imwrite(os.path.join(params.OUTPUT_DIR,
                                 'labled_image.png'), self.image_org)
        cv2.imshow('image_with node', self.image_org)
        cv2.waitKey(0)

    def write_bb_csv(self):
        # write node data to csv file
        filename = os.path.join(params.OUTPUT_DIR, "label_data.csv")
        fields = ['nodeNumber', 'nodeCenter', 'nodeRectC1', 'nodeRectC2']
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(self.bb_centers)

    def label_image(self, image_path):
        self.read_image(image_path)
        while True:
            cv2.imshow("image", self.image_temp)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):
                self.image = self.image_org.copy()
                self.image_temp = self.image_org.copy()
                self.captured_bb = []
            elif key == ord("u"):
                self.image = self.image_previous.copy()
                self.image_temp = self.image_previous.copy()
                cv2.imshow("image", self.image_temp)
                del self.captured_bb[-2:]
            elif key == ord("q"):
                break
        self.find_bb_center()
        self.save_labeled_images()
        self.write_bb_csv()
