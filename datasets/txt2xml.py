#!/usr/bin/env python
# Copyright (c) Baidu apollo, Inc.
# All Rights Reserved

# encoding:utf-8
from xml.dom.minidom import Document
import cv2
import os
import sys


def generate_xml(name, split_lines, img_size, class_ind):
    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    title = doc.createElement('folder')
    title_text = doc.createTextNode('KITTI')
    title.appendChild(title_text)
    annotation.appendChild(title)
    img_name = name+'.jpg'
    title = doc.createElement('filename')
    title_text = doc.createTextNode(img_name)
    title.appendChild(title_text)
    annotation.appendChild(title)
    source = doc.createElement('source')
    annotation.appendChild(source)
    title = doc.createElement('database')
    title_text = doc.createTextNode('The KITTI Database')
    title.appendChild(title_text)
    source.appendChild(title)
    title = doc.createElement('annotation')
    title_text = doc.createTextNode('KITTI')
    title.appendChild(title_text)
    source.appendChild(title)
    size = doc.createElement('size')
    annotation.appendChild(size)
    title = doc.createElement('width')
    title_text = doc.createTextNode(str(img_size[1]))
    title.appendChild(title_text)
    size.appendChild(title)
    title = doc.createElement('height')
    title_text = doc.createTextNode(str(img_size[0]))
    title.appendChild(title_text)
    size.appendChild(title)
    title = doc.createElement('depth')
    title_text = doc.createTextNode(str(img_size[2]))
    title.appendChild(title_text)
    size.appendChild(title)
    for split_line in split_lines:
        line = split_line.strip().split()
        if line[0] in class_ind:
            object = doc.createElement('object')
            annotation.appendChild(object)
            title = doc.createElement('name')
            title_text = doc.createTextNode(line[0])
            title.appendChild(title_text)
            object.appendChild(title)
            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            title = doc.createElement('xmin')
            title_text = doc.createTextNode(str(int(float(line[4]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('ymin')
            title_text = doc.createTextNode(str(int(float(line[5]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('xmax')
            title_text = doc.createTextNode(str(int(float(line[6]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('ymax')
            title_text = doc.createTextNode(str(int(float(line[7]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
    f = open('./annotations/'+name+'.xml', 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  creating new folder...  ---")
        print("---  finished creating ---")
    else:
        print("---  pass to create new folder ---")


if __name__ == '__main__':
    class_ind = ('Car', 'Cyclist', 'Truck', 'Van', 'Pedestrian', 'Tram')  # TODO: need to change
    cur_dir = os.getcwd()
    anno_dir = "annotations"
    mkdir(anno_dir)
    labels_dir = os.path.join(cur_dir, 'label_2')
    i = 0

    for parent, dirnames, filenames in os.walk(labels_dir):
        for file_name in filenames:
            full_path = os.path.join(parent, file_name)
            f = open(full_path)
            split_lines = f.readlines()
            name = file_name[:-4]
            img_name = name+'.png'  # TODO: need to change
            img_path = os.path.join('./image_2', img_name)  # TODO: change image path
            img_size = cv2.imread(img_path).shape
            generate_xml(name, split_lines, img_size, class_ind)
            i += 1
            print("\r", end="|")
            percent = i/len(filenames)*100
            print("processing: {:.4} % ".format(percent, '.2f'), end="")
            sys.stdout.flush()
            generate_xml(name, split_lines, img_size, class_ind)
            
print('\n' + 'all txts have converted into xmls')
