import os

import cv2
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import matplotlib.pyplot as plt
from pprint import pprint
import time

def get_box(index, box):
    final_box = []
    final_box.append(index)
    left_w = int(max(box[0][0], box[3][0]))
    final_box.append(left_w)
    left_h = int(max(box[0][1], box[1][1]))
    final_box.append(left_h)
    right_w = int(min(box[1][0], box[2][0]))
    final_box.append(right_w)
    right_h = int(min(box[2][1], box[3][1]))
    final_box.append(right_h)
    return final_box

def adjust_rectangle(final_boxes, final_txts):
    sorted_final_boxes = sorted(final_boxes, key=(lambda x: x[3]),reverse=True)
    sorted_final_txts = []
    for sorted_final_box in sorted_final_boxes:
        sorted_final_txts.append(final_txts[ sorted_final_box[0] ])
    return sorted_final_boxes, sorted_final_txts

def draw_adjust_rectangle(imagePath, sorted_final_boxes, outputPath, num, type, sorted_final_txts):
    img = cv2.imread(imagePath)
    index = 0
    for sorted_final_box in sorted_final_boxes:
        index += 1
        cv2.rectangle(img,(sorted_final_box[1],sorted_final_box[2]),(sorted_final_box[3],sorted_final_box[4]),(0,255,0),1)
        cv2.putText(img, str(index), (sorted_final_box[1], sorted_final_box[2]), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)


    # 写入调整以后的结果
    fileName = 'adjusted_OCRImageOutput_' + str(num) + '.txt'
    fileName = os.path.join(outputPath, fileName)
    if (os.path.exists(os.path.join(outputPath, fileName))):
        os.remove(os.path.join(outputPath, fileName))
        f = open(os.path.join(outputPath, fileName), 'w')
    else:
        f = open(os.path.join(outputPath, fileName), 'w')
    for sorted_final_txt in sorted_final_txts:
        f.write(sorted_final_txt)
        f.write('\n')
    print('写入调整以后的竖排版文字完成......')

    # 图片和pdf不同的保存路径
    if(type == 'imageOCR'):
        pictureName = os.path.join('./test', 'adjusted_OCR_img_' + str(num) + '.jpg')
    if (type == 'pdfOCR'):
        pictureName = os.path.join('./test', 'adjusted_OCR_pdf_' + str(num) + '.jpg')
    cv2.imwrite(pictureName, img)
    print('保存调整以后的竖排版图片完成......')


def is_vertical_word(sorted_final_boxes):
    total_num = 0
    vertical_num = 0
    for sorted_final_box in sorted_final_boxes:
        total_num += 1
        if((sorted_final_box[4] - sorted_final_box[2]) > (sorted_final_box[3] - sorted_final_box[1])):
            vertical_num += 1
    if(vertical_num > int(total_num / 2)):
        return True
    else:
        return False

class ClassA :
    def __init__(self) -> None:
        self.ocr = PaddleOCR()

     


def chi_sim_OCR(img_ndarray, num, type,  total_num, rate):

    ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, det_model_dir = "./det_infer",cls_model_dir="./cls_infer",rec_model_dir="./rec_infer")
    result = ocr.ocr(img_ndarray, cls=True)

    final_boxes = []
    final_txts = []
    index = 0
    for line in result:
        final_boxes.append(get_box(index, line[0]))
        index += 1
        final_txts.append(line[1][0])
    
if __name__ == "__main__":
    imagePath = "./xjp.png"
    chi_sim_OCR(img_ndarray= imagePath, num=1, type='imageOCR', rate=1)

