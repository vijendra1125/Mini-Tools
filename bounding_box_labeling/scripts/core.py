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
    def __init__(self):
        self.captured_bb = []
        self.top_left_captured = False
        self.first_intermediate_drawn = True
        self.last_mouse_pos = (0, 0)
        self.bb_border_width = 2
        self.bb_color = (0, 255, 0)

    def __del__(self):
        cv2.destroyallwindows()

    def read_image(self, image_path):
        self.image_org = cv2.imread(image_path)
        self.image_org = cv2.resize(self.image_org, dsize=(0, 0),
                                    fx=params.SCALE_FACTOR, fy=params.SCALE_FACTOR)
        self.image = self.image_org.copy()
        self.image_temp = self.image_org.copy()

    # def undo_image(self):

    def capture_bb(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.captured_bb.append((x, y))
            self.top_left_captured = True
        elif event == cv2.EVENT_LBUTTONUP:
            left = min(self.captured_bb[-1][0], x)
            right = max(self.captured_bb[-1][0], x)
            top = min(self.captured_bb[-1][1], y)
            bottom = max(self.captured_bb[-1][1], y)
            self.captured_bb[-1] = (left, top)
            self.captured_bb.append((right, bottom))
            cv2.rectangle(self.image,
                          self.captured_bb[-2], self.captured_bb[-1],
                          self.bb_color, self.bb_border_width)
            cv2.imshow(self.image_name, self.image)
            self.top_left_captured = False
            self.first_intermediate_drawn = True
        elif self.top_left_captured:
            if not self.first_intermediate_drawn:
                left = min(
                    self.captured_bb[-1][0], self.last_mouse_pos[0])-self.bb_border_width
                right = max(
                    self.captured_bb[-1][0], self.last_mouse_pos[0])+self.bb_border_width
                top = min(
                    self.captured_bb[-1][1], self.last_mouse_pos[1])-self.bb_border_width
                bottom = max(
                    self.captured_bb[-1][1], self.last_mouse_pos[1])+self.bb_border_width
                self.image[top:bottom, left:right] = \
                    self.image_org[top:bottom, left:right]
            cv2.rectangle(self.image,
                          self.captured_bb[-1], (x, y),
                          self.bb_color, self.bb_border_width)
            cv2.imshow(self.image_name, self.image)
            self.first_intermediate_drawn = False
            self.last_mouse_pos = (x, y)

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
        filename = os.path.join(params.OUTPUT_DIR, "label_data.csv")
        fields = ['nodeNumber', 'nodeCenter', 'nodeRectC1', 'nodeRectC2']
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(self.bb_centers)

    def label_image(self):
        image_names = os.listdir(params.DATA_DIR)
        for self.image_name in image_names:
            image_path = os.path.join(params.DATA_DIR, self.image_name)
            self.read_image(image_path)
            cv2.namedWindow(self.image_name)
            cv2.setMouseCallback(self.image_name, self.capture_bb)
            while True:
                cv2.imshow(self.image_name, self.image)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("r"):
                    self.image = self.image_org.copy()
                    self.captured_bb = []
                elif (key == ord("u")) and (len(self.captured_bb) != 0):
                    row_up = self.captured_bb[-2][1]-self.bb_border_width
                    row_down = self.captured_bb[-1][1]+self.bb_border_width
                    col_left = self.captured_bb[-2][0]-self.bb_border_width
                    col_right = self.captured_bb[-1][0]+self.bb_border_width
                    self.image[row_up:row_down, col_left:col_right] = \
                        self.image_org[row_up:row_down, col_left:col_right]
                    cv2.imshow(self.image_name, self.image)
                    del self.captured_bb[-2:]
                elif key == ord("n"):
                    break
            self.find_bb_center()
            if params.SAVE_LABELED:
                self.save_labeled_images()
            self.write_bb_csv()
