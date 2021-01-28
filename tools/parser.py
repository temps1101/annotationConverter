'''
Annotation file parser script
'''

import cv2


def yoloParser(filename, imgname):
    WIDTH, HEIGHT, _ = cv2.imread(imgname).shape

    with open(filename) as f:
        origin = f.readlines()

    try:
        origin.remove('')
    except ValueError:
        pass

    origin_list = list()
    for line in origin:
        class_idx, x, y, w, h, _ = line.split(' ')

        x = round(x * WIDTH)
        y = round(y * HEIGHT)
        w = round(w * WIDTH)
        h = round(h * HEIGHT)

        origin_list.append([class_idx, x, y, w, h])

    return origin_list
