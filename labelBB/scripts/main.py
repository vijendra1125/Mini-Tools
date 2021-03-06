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
    labeler = core.bb_labeling(params.LABEL_DICT)
    labeler.label_images()


if __name__ == '__main__':
    main()
