#!/usr/bin/env python
# Copyright (c) Baidu apollo, Inc.
# All Rights Reserved

import glob
import xml.etree.ElementTree as ET
from shutil import copyfile
import os
import sys

class_names = ['Car', 'Cyclist', 'Truck', 'Van', 'Pedestrian', 'Tram']  # need to change

# xml file path
path = './annotations/'
new_label_dir = "./labels/"


def single_xml_to_txt(xml_file):
    """
    cover xml to txt
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    txt_file = xml_file.split('.')[0]+'.txt'
    file = xml_file.split(path)[1].split('.')[0]+'.txt'
    with open(txt_file, 'w') as f:
        for member in root.findall('object'):
            # filename = root.find('filename').text
            picture_width = int(root.find('size')[0].text)
            picture_height = int(root.find('size')[1].text)
            class_name = member[0].text
            # 类名对应的index
            class_num = class_names.index(class_name)

            box_x_min = int(member[1][0].text)  # left top x
            box_y_min = int(member[1][1].text)  # right top y
            box_x_max = int(member[1][2].text)
            box_y_max = int(member[1][3].text)
            # cover to 2d bbox center and width / height
            x_center = float(box_x_min + box_x_max) / (2 * picture_width)
            y_center = float(box_y_min + box_y_max) / (2 * picture_height)
            width = float(box_x_max - box_x_min) / picture_width
            height = float(box_y_max - box_y_min) / picture_height

            f.write(str(class_num) + ' ' + str(x_center) + ' ' +
                    str(y_center) + ' ' + str(width) + ' ' + str(height) + '\n')
    copyfile(txt_file, new_label_dir + file)

# cover xml to txt


def dir_xml_to_txt(path):
    i = 0
    for xml_file in glob.glob(path + '*.xml'):
        single_xml_to_txt(xml_file)
        i += 1
        print("\r", end="|")
        print("processing: {} files: ".format(i), end="|")
        sys.stdout.flush()
    print('\n' + "Done")


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  creating new folder...  ---")
        print("---  finished  ---")
    else:
        print("---  pass to create new folder ---")


mkdir(new_label_dir)
dir_xml_to_txt(path)
