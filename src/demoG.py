import win32gui
import win32con
import pyautogui
import numpy as np
import utils.gameOCR as aocr
from paddleocr import PaddleOCR, draw_ocr
from PIL import ImageGrab, ImageShow, Image



if __name__ == '__main__':
    honkai3 = aocr.getTitleNumber('崩坏3')
    aocr.setActive(honkai3)

    image = np.array(aocr.getScreenshot(honkai3))
    ocr = PaddleOCR(
        use_angle_cls=True,
        show_log=False,
        lang="ch"
    )
    result = ocr.ocr(image, cls=True)

    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    
    image = draw_ocr(image, boxes)
    image = Image.fromarray(image)
    
    for i in txts:
        print(i)
    image.show()