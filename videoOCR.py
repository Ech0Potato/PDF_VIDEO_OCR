import  shutil
import cv2
import os
import win32gui
import  chineseOCR, firstFrame_1,videoOutput

def delete_frames(capturePath):
    for frame in os.listdir(capturePath):
        os.remove(os.path.join(capturePath, frame))


def video_capture_OCR(videoPath, outputPath):
    # 视频每帧的截图放在这里
    if(os.path.exists('./videoCapture')):
        for i in os.listdir('./videoCapture'):
            os.remove(os.path.join('./videoCapture', i))
    else:
        os.mkdir('./videoCapture')
    print('文件夹清空......')

    print('第一帧图片画框......')
    first_ix, first_iy, first_x, first_y, second_ix, second_iy, second_x, second_y = firstFrame_1.get_rectangle(videoPath=videoPath)
    print('第一帧图片画框完成......')

    cap = cv2.VideoCapture(videoPath)
    frameNum = 0
    print('开始播放视频......')
    rate = cap.get(5)
    print('视频播放速度{}帧/秒'.format(rate))
    while cap.isOpened():
        frameNum += 1
        frameName1 = 'videoCapture_1_' + str(frameNum) + '.jpg'
        frameName1 = os.path.join('./videoCapture', frameName1)
        frameName2 = 'videoCapture_2_' + str(frameNum) + '.jpg'
        frameName2 = os.path.join('./videoCapture', frameName2)
        ret, frame = cap.read()

        if (ret):
            cv2.rectangle(frame, (first_ix, first_iy), (first_x, first_y), (0, 255, 0), 1)
            cv2.rectangle(frame, (second_ix, second_iy), (second_x, second_y), (0, 255, 0), 1)
            img1 = frame[first_iy: first_y, first_ix:first_x]
            cv2.imwrite(frameName1, img1)
            img2 = frame[second_iy:second_y, second_ix:second_x]
            cv2.imwrite(frameName2, img2)
            print('第%d帧截取完毕' % frameNum)
            cv2.imshow('frame', frame)




        if cv2.waitKey(40)  & 0xFF == 27:
            break
        if win32gui.FindWindow(None, 'frame'):
            pass
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    # 清除保存视频帧识别结果的路径
    if(os.path.exists('./test')):
        for i in os.listdir('./test'):
            if (i.find('video') >= 0):
                os.remove(os.path.join('./test', i))
    else:
        os.mkdir('./test')
    print('清楚历史记录......')

    # 图片总数
    total_frame_num = 0
    for img in os.listdir('./videoCapture'):
        total_frame_num += 1


    # 创建保存结果的txt
    fileName = 'OCRVideoOutPut_' + str(total_frame_num) + '.txt'
    if (os.path.exists(os.path.join(outputPath, fileName))):
        os.remove(os.path.join(outputPath, fileName))
        f = open(os.path.join(outputPath, fileName), 'w')
    else:
        f = open(os.path.join(outputPath, fileName), 'w')


    # 对每一帧图片OCR
    frameNum = 0
    for img in os.listdir('./videoCapture'):
        frameNum += 1
        imgPath = os.path.join('./videoCapture', img)
        chineseOCR.chi_sim_OCR(imgPath, frameNum, 'videoOCR', outputPath=outputPath, total_num= total_frame_num, rate= rate)
        print('识别完成第%d张videoCapture......'% frameNum)

    '''
    处理结果
    '''
    '''
        videoOCR 进行提取首次出现的时间操作
    '''
    fileName = 'OCRVideoOutPut_' + str(total_frame_num) + '.txt'
    videoOutput.get_video_output(os.path.join(outputPath, fileName), outputPath, rate)

    # 把中间保存的每一帧截图，删除
    delete_frames('./videoCapture')

if __name__ == '__main__':
    videoPath = 'video1.mp4'
    videoPath = os.path.join(r'E:\OCR\code\test','video1.mp4')
    video_capture_OCR(videoPath=videoPath)

# 009 框1和2出问题了