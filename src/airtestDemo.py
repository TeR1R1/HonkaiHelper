import utils.gameOCR as aocr
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
    
    inst = [
        ['补给', (0, 0, GAME_WIDTH, GAME_HEIGHT)],
        ['前往商店', (0, 0, GAME_WIDTH, GAME_HEIGHT)]
    ]
    touch(
        (1109, 476)
    )
    doInst(inst[1])
    
    pyautogui.moveTo(
        x=797,
        y=676,
        duration=0.5
    )
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(
        x=797,
        y=36,
        duration=0.5
    )
    pyautogui.mouseUp(button='left')
    
    image = np.array(aocr.getScreenshot(honkai3))
    gold_im = np.array(Image.open('tmp/gold_shop.png'))
    matcher = TemplateMatching(
        im_search=gold_im,
        im_source=image,
        rgb=False
    )
    matcher.threshold = 0.6
    
    res = matcher.find_all_results()
    print(res)
    if res != None:
        for i in range(len(res)):
            touch(
                v=Template(
                    filename=r'tmp/gold_shop.png',
                    target_pos=5,
                    threshold=0.6
                )
            )
            checkGood()
    
    # shopGold = KeypointMatching(
    #     im_source=gold_im,
    #     im_search=image,
    # )
    # shopGold.threshold = 0.6
    # shopGold.show_match_image()
    
    # print(res)
    
    
    # find_all_sift(
    #     im_source=image,
    #     im_search=gold_im,
    #     threshold=0.8,
    #     rgb=True
    # )
    # res = 0
    # l = [698, 342, 735, 383]
    
    # for i in res:
    #     print(i)
    
    # for gold in res:
    #     mask_image(
    #         img=image,
    #         mask=gold['rectangle'][0] + gold['rectangle'][2],
    #         color=(255, 0, 0),
    #         linewidth=5
    #     )
    
    # image = Image.fromarray(image)
    # image.show()
    
