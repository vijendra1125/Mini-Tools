# Bounding box labeling

## About
A tool label images with bounding box and saving annotation in csv file.

Currently available features:
* Choose between labeling from scratch and labeling on top of saved annotations 
* Label a large number of classes
* Navigate between images while labeling
* Switch between classes to label
* Unlimited undo
* Reset image label

## How to use
* Edit parameters.py
* Run main.py

## Reserved keys:
| key | function                                 |
| --- | ---------------------------------------- |
| c   | clear the complete labeling on the image |
| u   | undo                                     |
| n   | go to next image                         |
| p   | go to previous image                     |
| f   | finish labeling                          |

Apart from above key, any other key could be assigned to defined class

## Dependencies 
* Python 3.7.4
* OpenCV 4.2.0
* Csv 1.0
* Numpy 1.18.1

## TODO
* Cleanup, refactoring and comment

## Features in Future
* Deleting previously added bounding box
* Display bounding box ID
* add info display board
* Providing GUI