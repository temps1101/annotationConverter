'''
Annotation file parser script
'''

import glob
import os
import cv2


def yoloParser(input_dir):
    files = glob.glob(os.path.join(input_dir, '*.txt'))

    objects = list()
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

        objects.append(annotations)

    return objects
