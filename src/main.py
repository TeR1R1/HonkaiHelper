import sys, os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

import numpy as np
import cv2

from PIL import Image

from moduld.automation.screenshot import Screenshot
from moduld.automation.autotools import Autotools
from moduld.automation.input import Input

if __name__ == '__main__':
    test_window_title = 'QQ'
    Screenshot.set_before_title(test_window_title)
    autotools = Autotools(test_window_title)
    autotools.take_screenshot(max_try_count=1)
    if autotools.screenshot:
        # Screenshot.show_screenshot(autotools.screenshot)
        Screenshot.save_screenshot(autotools.screenshot, 'tmp/test1.png')
    
    test1 = cv2.imread('tmp/test1.png')
    test1_template = cv2.imread('tmp/wife_icon.png', cv2.IMREAD_UNCHANGED)
    
    # Image.fromarray(np.array(autotools.screenshot)).show()
    # Image.fromarray(np.array(test1_template)).show()

    left_top, right_bottom, _ = autotools.find_image_element('tmp/wife_icon.png', 0.95)
    test1_count = autotools.find_image_and_count('tmp/wife_icon.png', 0.8)
    print(test1_count)
    
    # if left_top:
    #     Input.mouse_click((left_top[0] + right_bottom[0]) // 2, (left_top[1] + right_bottom[1]) // 2)