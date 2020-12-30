import base64
import numpy as np
import pytesseract
import cv2

fin = open("base64_in.txt","rb")
data = fin.read()
fin.close()

fout = open("base64.png", "wb")
fout.write(base64.decodebytes(data))
fout.close()

imgOri = cv2.imread("base64.png")
height, width, numChannels = imgOri.shape
bordersize = 32
border = cv2.copyMakeBorder(
    imgOri,
    top=bordersize,
    bottom=bordersize,
    left=bordersize,
    right=bordersize,
    borderType=cv2.BORDER_CONSTANT,
    value=[255, 255, 255]
)
imgOri = border
height, width, numChannels = imgOri.shape
imgGray = np.zeros((height, width, 1), np.uint8)
imgGray = cv2.cvtColor(imgOri, cv2.COLOR_RGB2GRAY)
imgGray = cv2.resize(imgGray, (0, 0), fx = 1.6, fy = 1.6)
#imgGray = cv2.bitwise_not(imgGray)

# Image Conditioning to remove noise and maintain edges
imgBlurred = np.zeros((height, width, 1), np.uint8)
imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)
#imgBlurred = cv2.bitwise_not(imgBlurred)

custom_config = r'--psm 4 --oem 3'
ocr_text = pytesseract.image_to_string(imgBlurred, config=custom_config)
#ocr_text = pytesseract.image_to_string(imgBlurred, lang="ind", config=custom_config)

buffer = ""
old_value = 10
for q in range(len(ocr_text)):
    value = ord(ocr_text[q])

    if ((value >= 32 and value < 127) or value == 10):
        if(value == 10 and old_value == 10):
            pass
        else:
            buffer += ocr_text[q]  # buffer diisi char readable
        old_value = value
ocr_text = buffer
buffer = ""
c_mode = False
for q in range(len(ocr_text)):
    value = ord(ocr_text[q])

    if c_mode:
        if(value == 32):
            if((q+1) < len(ocr_text)):
                next = ord(ocr_text[q+1])
                if(next >= 48 and next <= 57):
                    buffer += '.'
                else:
                    prev = ord(buffer[-3])
                    if(prev != 46):
                        buffer = buffer[:-2] + '.' + buffer[-2:]
                        print(buffer[-2:])
                    buffer += ' '
            else:
                buffer += ocr_text[q]
            c_mode =  False
        elif(value == 46):
            buffer += ocr_text[q]
            c_mode =  False
        elif(value == 10):
            prev = ord(buffer[-3])
            if(prev != 46):
                buffer = buffer[:-2] + '.' + buffer[-2:]
                print(buffer[-2:])
            buffer += ocr_text[q]
            c_mode =  False
        else:
            buffer += ocr_text[q]
    else:
        buffer += ocr_text[q]
        if(value == 75):
            c_mode = True

buffer = buffer.replace('KO0.','K0.')
buffer = buffer.replace('KO.','K0.')

# rewrite variable
ocr_text = buffer

fout = open("base64_out.txt","w")
fout.write(ocr_text)
fout.close()
