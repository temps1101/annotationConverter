'''
Main script of the annotation converter.
===
The flow of this converter:

1. Make a unified annotation file using this script.
2. Generate other types of annotations with different format.
'''


import argparse
import pickle

import tools


def get_args():
    '''
    Argument parser func.
    '''

    parser = argparse.ArgumentParser(description='AnnotationConverter: Converts the annotation format for the object detection dataset')  # noqa: E501
    parser.add_argument('-m' '--mode', dest='mode', choices=['parse', 'gen'], required=True, help='Toggles the mode from \'parse\' and \'gen\'')  # noqa: E501
    parser.add_argument('-f', '--format', dest='format', choices=['yolo', 'voc'], required=True, help='Toggles the format of the annotation from \'yolo\' and \'voc\'')  # noqa: E501
    parser.add_argument('-d', '--directory', dest='directory', type=str, required=True, help='The main directory you are going to use. For the mode \'parse\', this will be the input directory and for the mode \'gen\', this will be the output directory.')  # noqa: E501

    parser.add_argument('--cls_file', dest='cls_file', type=str, required=False, help='The file path of the annotation. Use with voc.')  # noqa: E501
    parser.add_argument('--output_file', default='.', dest='output_file', type=str, required=False, help='The file directory of the output file. Use with parse mode.')  # noqa: E501


def dump_dict(annotation_dict, filename):
    '''Dumps the annotation information to a file.

    Args:
        annotation_dict (dict): Annotation dict
        filename (str): Path to save the annotation file.
    '''

    with open(filename, 'wb') as f:
        pickle.dump(annotation_dict, f)

    print('saved annotation info to {}'.format(filename))


def main(args):
    '''
    Main function of the script
    '''

    if args.mode == 'parse':
        if args.format == 'yolo':
            objects = tools.annotation_parser.yoloParser(args.directory)
            dump_dict(objects, args.output_file)

        if args.format == 'voc':
            objects = tools.annotation_parser.vocParser(args.directory, args.cls_file)  # noqa: E501
            dump_dict(objects, args.output_file)


if __name__ == '__main__':
    args = get_args()
    main()
