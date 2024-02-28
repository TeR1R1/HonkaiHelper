import logging
import random
import re
import pyautogui
import numpy as np
from models.utils.gameOCR import *
from airtest.core.api import *

'''

进入家园，领家园福利，挂打工。

'''

imFilePath = 'src/data/imdata/家园/'

inst = {
    '家园': [
        (1060, 660, 1182, 707),
        random.randint(1060, 1111),
        random.randint(660, 690)
    ],
    '打工': [
        (900, 650, 1060, 740),
        random.randint(958, 1020),
        random.randint(668, 706)
    ],
    '金币': [
        (315, 191, 471, 386),
        random.randint(315, 471),
        random.randint(191, 386)
    ],
    '体力': [
        (168, 242, 279, 373),
        random.randint(168, 279),
        random.randint(242, 373)

    ],
    '取出体力': [
        (700, 565, 831, 607),
        random.randint(700, 831),
        random.randint(565, 607)
    ],
    '展开打工列表': [
        (1200, 330, 1282, 497),
        random.randint(1243, 1273),
        random.randint(366, 406)
    ],
    '已完成': [
        (835, 38, 1278, 188),
        random.randint(835, 1278),
        random.randint(38, 188)
    ],
    '确定': [
        (601, 551, 689, 596),
        random.randint(601, 689),
        random.randint(551, 596)
    ],
    '取消': [
        (476, 429, 556, 470),
        random.randint(476, 556),
        random.randint(429, 470)
    ]
}


def sleepRand():
    sleep(random.random() * 0.5 + 0.5)


def ocrTouch(a):
    image = np.array(getScrPart(inst[a][0]))
    if ocrCheck(a, image):
        pyautogui.click(
            x=inst[a][1],
            y=inst[a][2],
            duration=0.5,
            interval=0.2
        )
    else:
        print('INFO: 未执行。')


def imTouch(a):
    im_source = np.array(getScrPart(inst[a][0]))
    im_search = np.array(Image.open(f'{ imFilePath }{ a }.png'))
    if imCheck(im_source, im_search):
        pyautogui.click(
            x=inst[a][1],
            y=inst[a][2],
            duration=0.5,
            interval=0.2
        )
    else:
        print('INFO: 未执行。')


def wordStart():
    connect_device("Windows:///?title=崩坏3")

    ocrTouch('家园')
    sleepRand()

    touch(
        v=Template(
            filename=imFilePath + '金币罐.png'
        ),
        times=2,
    )
    sleepRand()
    touch(
        v=Template(
            filename=imFilePath + '体力罐.png'
        )
    )
    sleepRand()

    ocrTouch('取出体力')
    sleepRand()
    pyautogui.click(button='left')
    sleepRand()

    ocrTouch('打工')
    imTouch('展开打工列表')

    pyautogui.moveTo(
        x=1050, y=189,
        duration=0.5
    )
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(
        x=1050, y=645,
        duration=0.2
    )
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(
        x=1050, y=189,
        duration=0.5
    )
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(
        x=1050, y=645,
        duration=0.2
    )
    pyautogui.mouseUp(button='left')
    sleepRand()

    image = np.array(getScrPart(inst['已完成'][0]))
    while ocrCheck('已完成', image):
        pyautogui.click(
            x=inst['已完成'][1],
            y=inst['已完成'][2],
            duration=0.2,
            interval=0.1
        )
        ocrTouch('确定')
        sleepRand()
        image = np.array(getScrPart(inst['已完成'][0]))
    

    
    
    # 识别饭团
    max_attempts = 3 # 最大重试次数
    for i in range(max_attempts):
        image = np.array(getScrPart((554, 687, 637, 720)))
        txt = ocrText(image)[0]
        try:
            numbers = [int(num) for num in re.findall(r'\d+', txt)]
            if len(numbers) == 2:
                l, r = numbers
                break
            else:
                raise ValueError(f'\033[31mERROR:\033[0m饭团数值出错！({i + 1}/3)')
        except:
            print(f'\033[31mERROR:\033[0m识别饭团数值失败！({i + 1}/3)')

    # 返回主页面
    image = np.array(getScrPart(inst['取消'][0]))
    while not ocrCheck('取消', image):
        pyautogui.press('`')
        sleepRand()
        image = np.array(getScrPart(inst['取消'][0]))
    ocrTouch('取消')


if __name__ == '__main__':
    # 调整 'airtest' 的日志等级
    logger = logging.getLogger("airtest")
    logger.setLevel(logging.ERROR)
    
    honkai3 = getTitleNumber('崩坏3')
    setActive(honkai3)

    wordStart()
    print('INFO: \033[1;32m家园模块运行完毕！\033[0m')
