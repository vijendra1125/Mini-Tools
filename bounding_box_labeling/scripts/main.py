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
    label_class_dict = {'r': [0, 'red', (0, 0, 255)],
                        'g': [1, 'green', (0, 255, 0)],
                        'b': [2, 'blue', (255, 0, 0)]}
    core.bb_labeling.start_new()
    labeler = core.bb_labeling(label_class_dict)
    labeler.label_images()


if __name__ == '__main__':
    main()
