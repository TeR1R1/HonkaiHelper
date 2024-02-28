import win32gui
import win32con
import numpy as np
from airtest.aircv.template_matching import *
from paddleocr import PaddleOCR
from PIL import ImageGrab, Image

GAME_WIDTH = 1600
GAME_HEIGHT = 900
SCALE_FACTOR_X = 1.0
SCALE_FACTOR_Y = 1.0

def getTitleNumber(winTitle):
    return win32gui.FindWindow(None, winTitle)


def setActive(hwnd):
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE
    )


def getScreenshot(hwnd):
    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab((x1, y1, x2, y2))
    return screenshot


def getScrPart(pos):
    return ImageGrab.grab(pos)


def gameOCR(image):
    ocr = PaddleOCR(
        use_angle_cls=True,
        show_log=False,
        lang="ch"
    )
    result = ocr.ocr(image, cls=True)

    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    print(f'OCROUT: { txts }')
    return boxes, txts

def ocrCheck(txt, image):
    ocr = PaddleOCR(
        use_angle_cls=True,
        show_log=False,
        lang="ch"
    )
    result = ocr.ocr(image, cls=True)

    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    print(f'OCROUT: { txts }')
    
    for s in txts:
        if txt in s:
            return True
    return False

def ocrText(image):
    ocr = PaddleOCR(
        use_angle_cls=True,
        show_log=False,
        lang="ch"
    )
    result = ocr.ocr(image, cls=True)[0]
    txts = [line[1][0] for line in result]
    return txts

def imCheck(im_source, im_search, threshold = 0.8):
    matcher = TemplateMatching(
        im_search=im_search,
        im_source=im_source,
        rgb=True
    )
    matcher.threshold = threshold
    res = matcher.find_all_results()
    return False if res == None else True