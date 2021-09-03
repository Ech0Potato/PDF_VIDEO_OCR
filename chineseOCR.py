import os

import cv2
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import matplotlib.pyplot as plt

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



def chi_sim_OCR(imagePath, num, type, outputPath, total_num, rate):
    print('OCR image 路径是.....')
    print(imagePath)
    print("识别结果如下......")
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, det_model_dir = "./det_infer",cls_model_dir="./cls_infer",rec_model_dir="./rec_infer")
    result = ocr.ocr(imagePath, cls=True)
    if(type == 'imageOCR'):
        fileName = 'OCRImageOutput_' + str(num) + '.txt'
        if(os.path.exists(os.path.join(outputPath, fileName))):
            os.remove(os.path.join(outputPath, fileName))
            f = open(os.path.join(outputPath, fileName), 'w')
        else:
            f = open(os.path.join(outputPath, fileName), 'w')
    elif(type == 'pdfOCR'):
        fileName = 'OCRPdfOutPut_' + str(num) + '.txt'
        f = open(os.path.join(outputPath, fileName), 'w')
        # if (os.path.exists(os.path.join(outputPath, fileName))):
        #     os.remove(os.path.join(outputPath, fileName))
        #     f = open(os.path.join(outputPath, fileName), 'w')
        # else:
        #     f = open(os.path.join(outputPath, fileName), 'w')
    else:
        fileName = 'OCRVideoOutPut_' + str(total_num) + '.txt'
        # if (os.path.exists(os.path.join(outputPath, fileName))):
        #     os.remove(os.path.join(outputPath, fileName))
        #     f = open(os.path.join(outputPath, fileName), 'w')
        # else:
        #     f = open(os.path.join(outputPath, fileName), 'w')
        with open(os.path.join(outputPath, fileName), 'a', encoding='gbk') as f:
            if(num <= total_num / 2):
                f.write('OCR_video_rectangle_1_' + str(num) + '结果如下:')
                f.write('\n')
            else:
                f.write('OCR_video_rectangle_2_' + str(int(num - total_num / 2)) + '结果如下:')
                f.write('\n')

    final_boxes = []
    final_txts = []
    index = 0
    for line in result:
        final_boxes.append(get_box(index, line[0]))
        index += 1
        final_txts.append(line[1][0])
        print(line)
        print(line[1][0])
        print('写入识别结果......')
        if(type == 'videoOCR'):
            with open(os.path.join(outputPath, fileName), 'a', encoding='gbk') as f:
                f.write(line[1][0])
                f.write('|')
        else:
            with open(os.path.join(outputPath, fileName), 'a', encoding='gbk') as f:
                f.write(line[1][0])
                f.write('\n')


    # 识别结果写入完成以后，写入换行
    with open(os.path.join(outputPath, fileName), 'a', encoding='gbk') as f:
        f.write('\n')


    print('保存识别图片......')
    if(type == 'imageOCR'):

        if (os.path.exists('./test')):
            for i in os.listdir('./test'):
                if (i.find('img') >= 0):
                    os.remove(os.path.join('./test', i))
        else:
            os.mkdir('./test')

        save_ptah = os.path.join('./test', 'OCR_img_' + str(num) + '.jpg')
        # 保存图片识别结果的路径
        # if (os.path.exists(save_ptah)):
        #     os.remove(save_ptah)
    elif(type == 'videoOCR'):
        if (num <= total_num / 2):  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            save_ptah = os.path.join('./test', 'OCR_video_rectangle_1_' + str(num) + '.jpg')
        else:
            save_ptah = os.path.join('./test', 'OCR_video_rectangle_2_' + str(num - total_num / 2) + '.jpg')
    else:
        save_ptah = os.path.join('./test', 'OCR_pdf_' + str(num) + '.jpg')
    # print('识别结果图片保存路径{}'.format(save_ptah))
    # '''
    # paddleocr save
    # '''
    # image = Image.open(imagePath).convert('RGB')
    # boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores)
    # im_show = Image.fromarray(im_show)
    # im_show.save(save_ptah)
    # print('保存完成......')




    '''
    对竖排排版的图片修正
    '''
    sorted_final_boxes, sorted_final_txts = adjust_rectangle(final_boxes, final_txts)


    '''
    判断横排版还是竖排版
    '''
    vertical_word = is_vertical_word(sorted_final_boxes)
    if(vertical_word == False):
        print('此图片文字为横排版 识别结束 不需要后续操作......')
        return
    print('此图片文字为竖排版......')
    '''
    用修正以后的框画图
    '''
    if(type == 'imageOCR'):
        draw_adjust_rectangle(imagePath, sorted_final_boxes, outputPath, num, 'imageOCR', sorted_final_txts)
    if (type == 'pdfOCR'):
        draw_adjust_rectangle(imagePath, sorted_final_boxes, outputPath, num, 'pdfOCR', sorted_final_txts)


if __name__ == "__main__":
    imagePath = "./xjp.png"
    chi_sim_OCR(imagePath= imagePath, num=1, type='imageOCR', outputPath='./',total_num=1, rate=1)

