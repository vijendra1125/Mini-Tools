#
# Created on Sat Aug 29 2020
# Author: Vijendra Singh
# License: MIT
# Brief:
#

import os

import parameters as params
import core


def main():
    filename = os.path.join(params.OUTPUT_DIR, "label_data.csv")
    if os.path.exists(filename):
        os.remove(filename)
    core.bb_labeling.csv_init()

    # label red class in all images
    labeler_class3 = core.bb_labeling('red', (0, 0, 255))
    labeler_class3.label_image()
    # label green class in all images
    labeler_class1 = core.bb_labeling('green', (0, 255, 0))
    labeler_class1.label_image()
    # label blue class in all images
    labeler_class2 = core.bb_labeling('blue', (255, 0, 0))
    labeler_class2.label_image()


if __name__ == '__main__':
    main()
