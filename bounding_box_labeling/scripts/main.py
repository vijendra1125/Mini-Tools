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
    image_names = os.listdir(params.DATA_DIR)
    labler = core.bb_labeling('labler')
    for image_name in image_names:
        image_path = os.path.join(params.DATA_DIR, image_name)
        labler.label_image(image_path)


if __name__ == '__main__':
    main()
