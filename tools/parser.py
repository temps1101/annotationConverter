'''
Annotation file parser script
'''

import glob
import os
import cv2


def yoloParser(input_dir):
    '''Parses YOLO format annotation and returns a list of annotations

    ===
    Directory tree should be like this:

    input_dir
    ├─0.jpg # Image to use for the AI
    ├─0.txt # Text annotation file written in YOLO format of the image that
              has the same name.
    ...
    ===

    Args:
        input_dir (str): Directory of the annotation files.

    Returns:
        list: dictionary of annotations.
    '''

    files = glob.glob(os.path.join(input_dir, '*.txt'))

    objects = dict()
    for filename in files:
        imgname = filename.split('.')[0] + '.png'
        WIDTH, HEIGHT, _ = cv2.imread(imgname).shape

        with open(filename) as f:
            origin = f.readlines()

        try:
            origin.remove('')
        except ValueError:
            pass

        annotations = list()
        for line in origin:
            class_idx, x, y, w, h, _ = line.split(' ')

            x = round(x * WIDTH)
            y = round(y * HEIGHT)
            w = round(w * WIDTH)
            h = round(h * HEIGHT)

            annotations.append([class_idx, x, y, w, h])

        objects[filename] = annotations

    return objects
