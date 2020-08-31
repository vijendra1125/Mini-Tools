#
# Created on Sat Aug 29 2020
# Author: Vijendra Singh
# License: MIT
# Brief:
#

# directory containing images to label
DATA_DIR = '../data'
# directory to write labeling output
OUTPUT_DIR = '../output'
# true if labeling need to be done from scratch
START_NEW = False
# image file extension
FILE_EXT = ".jpg"
# dictionary defining class labels
# format - <key>:[<class ID>, <class name>, <class color>]
# check README.md for key which cant be assigned to class label
LABEL_DICT = {'r': [0, 'red', (0, 0, 255)],
              'g': [1, 'green', (0, 255, 0)],
              'b': [2, 'blue', (255, 0, 0)]}
# factor by which image should be scaled before labeling
SCALE_FACTOR = 1
