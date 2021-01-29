'''
Annotation file parser script
'''

import glob
import os
import xml.etree.ElementTree as et

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


def vocParser(annotation_dir, class_filename):
    '''Parses a VOC format xml annotation files.

    ===
    Directory tree must be like this:

    annotation_dir
    ├─000001.xml
    ├─000002.xml
    ...

    ===
    Args:
        annotation_dir (str): Directory where the annotation files are located.
        class_filename (str): Class file path.
    '''
    with open(class_filename) as f:
        classes = f.readlines()

    try:
        classes.remove('')
    except ValueError:
        pass

    files = glob.glob(os.path.join(annotation_dir, '*.xml'))

    objects = dict()
    for file in files:
        annotations = list()
        tree = et.parse(file)
        root = tree.getroot()

        imgname = root[1].text.split('.')[0]
        HEIGHT, WIDTH, _ = [e.text for e in root[4]]

        annotations = list()
        for objects in root[5:]:
            class_idx = classes.index(objects[0].text)

            x1, y1, x2, y2 = [int(e.text) for e in objects[4]]
            x = round((x1 + x2) / 2)
            y = round((y1 + y2) / 2)
            w = x2 - x1
            h = y2 - y1

            annotations.append([class_idx, x, y, w, h])

        objects[imgname] = annotations
