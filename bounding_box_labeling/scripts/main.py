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
    labeler = core.bb_labeling()
    labeler.label_image()


if __name__ == '__main__':
    main()
