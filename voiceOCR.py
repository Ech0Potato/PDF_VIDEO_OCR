import speech_recognition as sr
import os
import io


def voiceOCR(file):

    r = sr.Recognizer()
    harvard = sr.AudioFile(file.file)
    with harvard as source:
        all_audio = r.record(source)
        all_text = r.recognize_sphinx(all_audio,language='zh-CN')
        return all_text
    

# def voiceOCR(voicePath, outputPath):
#     print('voicePath is :{}'.format(voicePath))
#     print('outputPaht is :{}'.format(outputPath))
#     r = sr.Recognizer()
#     harvard = sr.AudioFile(voicePath)

#     with harvard as source:
#         all_audio = r.record(source)
#         print(type(all_audio))

#         all_text = r.recognize_sphinx(all_audio,language='zh-CN') #language=zh-CN
#         print(all_text)
#         if(os.path.exists(os.path.join(outputPath, 'voiceOutput.txt'))):
#             os.remove(os.path.join(outputPath, 'voiceOutput.txt'))
#             f = open(os.path.join(outputPath, 'voiceOutput.txt'), 'w')
#         else:
#             f = open(os.path.join(outputPath, 'voiceOutput.txt'), 'w')
#         with open(os.path.join(outputPath, 'voiceOutput.txt'), 'a') as f:
#             f.write(all_text)

# if __name__ == '__main__':
#     print(sr.__file__)
#     voicePath = './testing.wav'
#     voiceOCR(voicePath ,outputPath='/')