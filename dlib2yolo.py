'''
dlib .xml file to yolo .txt file 

python xml2txt.py dlib_train_path dlib_test_path 

example:
	python xml2txt.py /home/hichens/YOLOData/train/ /home/hichens/YOLOData/test/ 
'''

import cv2
import os 
import subprocess
import sys 
import random 
import string
import xml.etree.ElementTree as ET


class_dict = {'fireextinguisher': 0, 'exit': 1, 'chair': 2, 'trashbin': 3, 'clock': 4, 'screen': 5, 'printer': 6}  

data_path = sys.argv[1]
test_path = sys.argv[2]
# file_path = "/".join(train_path.split("/")[:-2])
label_list = []
# print(file_path)
# subprocess.run(['rm', '-rf',  file_path + "/JPEGImages/"])
# subprocess.run(['mkdir', "JPEGImages"])
# subprocess.run(['rm', '-rf',  file_path + "/labels/"])
# subprocess.run(['mkdir', "labels"])

def xml2txt(xml_path, num):
    # print(xml_path)

    mytree = ET.parse(xml_path)
    myroot = mytree.getroot()

    # print(myroot[2].tag)
    for image in myroot[2].findall('image'):
    # using root.findall() to avoid removal during traversal
        image_name = (image.attrib['file'])
        for box in (image.findall('box')):
            box_pos = box.attrib
            label = str(box.find('label').text)
            img = cv2.imread(os.path.join(data_path, num, image_name))
            top, left, width, height = int(box_pos['top']), int(box_pos['left']), int(box_pos['width']), int(box_pos['height'])
            # print(top, left, width, height)
            H, W = img.shape[:2]
            # print(H, W)
            x_center, y_center =  (left+width / 2)  / W, (top+height / 2) / H
            # print(x_center, y_center)
            w, h = width / W, height / H
            # print(w, h)
            file_name = os.path.join(data_path, num, image_name.replace('jpg','txt'))
            with open(file_name, 'a+') as file:
                match label:
                    case 'fireextinguisher':
                        sentence = " ".join(str(i) for i in [0, x_center, y_center, w, h])
                    case 'exit':
                        sentence = " ".join(str(i) for i in [1, x_center, y_center, w, h])
                    case 'chair':
                        sentence = " ".join(str(i) for i in [2, x_center, y_center, w, h])
                    case 'trashbin':
                        sentence = " ".join(str(i) for i in [3, x_center, y_center, w, h])
                    case 'clock':
                        sentence = " ".join(str(i) for i in [4, x_center, y_center, w, h])
                    case 'screen':
                        sentence = " ".join(str(i) for i in [5, x_center, y_center, w, h])  
                    case 'printer':
                        sentence = " ".join(str(i) for i in [6, x_center, y_center, w, h])  
                
                file.write(sentence + '\n')

    

    # print(base_path + '\n' +  I_path)
    # with open(xml_path, 'r') as f:
    #     for line in f:
    #         ss = line.split()
    #         print(ss)
    #         if(len(ss) < 1):
    #             pass
    #         else:
    #             if(ss[0] == "<image"):
    #                 img_name = line.split("'")[1]
    #                 print(img_name + "*******")
    #             if(ss[0] == "<box"):
    #                 ll = line.split("'")
    #                 top, left, width, height = int(ll[1]), int(ll[3]), int(ll[5]), int(ll[7])
    #                 # print(top, left, width, height)
    #                 img_path ='/media/roy/data1/ML_material/Indoor-Object-Detection-Dataset/sequence_1/' + img_name # image int the xieshi_train or xieshi_test
    #                 move_path = '/media/roy/data1/ML_material/Indoor-Object-Detection-Dataset' + "/JPEGImages/" + img_name 
    #                 # print(img_path)
    #                 # subprocess.run(['cp', img_path, move_path]) # move the image to JPEGImages
    #                 # add_label = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    #                 # new_name =  base_path + "/JPEGImages/" + add_label + '.jpg'
    #                 # os.rename(move_path, new_name) # rename the imgage in the JPEGImages

    #                 img = cv2.imread(img_path)
    #                 H, W = img.shape[:2]
    #                 x_center, y_center =  (left+width / 2)  / W, (top+height / 2) / H
    #                 w, h = width / W, height / H
    #                 # print(x_center, y_center, w, h)
    #                 file_name = '/media/roy/data1/ML_material/Indoor-Object-Detection-Dataset' + "/sequence_1/" + img_name.replace('.jpg','') +".txt" # accoding to image name in the JPEGImages name the txt
    #                 with open(file_name, 'w+') as file:
    #                     sentence = " ".join(str(i) for i in [0, x_center, y_center, w, h])
    #                     file.write(sentence + '\n')
                    # break
            
if __name__ == "__main__":

    for file in os.listdir(os.path.join(data_path, 'annotation')):
        if file[-4:] == '.xml':
            print(file)
            xml2txt(os.path.join(data_path, 'annotation', file), 'sequence_' + file[-5])

    # xml2txt(os.path.join(train_path, "annotation_s1.xml"))
    # xml2txt(test_path + "test.xml")
