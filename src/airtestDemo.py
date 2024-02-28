import models.utils.gameOCR as aocr
import numpy as np
from airtest.aircv.template import *
from airtest.aircv.aircv import *
from airtest.aircv.sift import *
from airtest.core.api import *
from airtest.aircv.template_matching import *
from demo import *
import pyautogui
from PIL import Image
from airtest.aircv.keypoint_base import KeypointMatching

if __name__ == '__main__':
    honkai3 = aocr.getTitleNumber('崩坏3')
    aocr.setActive(honkai3)
    x1, y1, x2, y2 = win32gui.GetWindowRect(honkai3)
    GAME_WIDTH, GAME_HEIGHT = int(x2), int(y2)

    connect_device("Windows:///?title=崩坏3")

    # image = np.array(aocr.getScreenshot(honkai3))
    # gold_im = np.array(Image.open('src/data/imdata/家园/体力罐.png'))
    image = snapshot()
    show(imread(image))
    
    
    # mask_image(
    #     img=image,
    #     mask=(100, 200, 500, 500),
    #     color=(255, 0, 0),
    #     linewidth=5
    # )

    # image = Image.fromarray(image)
    # image.show()
