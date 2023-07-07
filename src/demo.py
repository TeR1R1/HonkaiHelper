import win32gui
import win32con
import pyautogui
import time
import sys
import numpy as np
import utils.gameOCR as aocr

from paddleocr import PaddleOCR, draw_ocr
from PIL import ImageGrab, ImageShow, Image

GAME_WIDTH = 1600
GAME_HEIGHT = 900
SCALE_FACTOR_X = 1.0
SCALE_FACTOR_Y = 1.0


def checkGood():
    image = np.array(aocr.getScrPart((480, 525, 820, 620)))
    _, txts =  aocr.gameOCR(image)
    if '确定' in txts:
        print('INFO: 执行确定')
        pyautogui.press(
            keys='`',
            interval=0.5
        )


def doInst(inst):
    for i in range(3):
        image = np.array(aocr.getScrPart(inst[1]))
        boxes, txts = aocr.gameOCR(image)
        for i in range(len(txts)):
            if inst[0] in txts[i]:
                pyautogui.click(
                    int(boxes[i][0][0] + inst[1][0]),
                    int(boxes[i][0][1] + inst[1][1]),
                    interval=0.5,
                    duration=0.2
                )
                checkGood()
                return True
    print('INFO: 未找到目标。')
    return False


if __name__ == '__main__':
    honkai3 = aocr.getTitleNumber('崩坏3')
    aocr.setActive(honkai3)
    x1, y1, x2, y2 = win32gui.GetWindowRect(honkai3)
    GAME_WIDTH, GAME_HEIGHT = int(x2), int(y2)
    SCALE_FACTOR_X = x2 // 1280
    SCALE_FACTOR_Y = y2 // 750

    inst1 = [
        ['家园', (800, 625, GAME_WIDTH, GAME_HEIGHT)],
        ['打工', (800, 625, GAME_WIDTH, GAME_HEIGHT)],
        ['<', (1240, 313, 1270, 410)],
        ['已完成', (835, 38, 1278, 188)]
    ]
    
    if not doInst(inst1[0]):
        aocr.getScrPart(inst1[0][1]).show()
        sys.exit()
    if not doInst(inst1[1]):
        aocr.getScrPart(inst1[1][1]).show()
        sys.exit()
    doInst(inst1[2])
    while doInst(inst1[3]): pass

    # image = np.array(getScrPart(inst1[0][1]))
    # boxes, txts = gameOCR(image)
    # im_show = draw_ocr(image, boxes)
    # im_show = Image.fromarray(im_show)

    # im_show.show()
    # im_show.save('./tmp/demo.png')
    # getScreenshot(honkai3).show()
