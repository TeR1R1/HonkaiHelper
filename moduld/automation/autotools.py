import numpy as np
import logging
import time
import math
import cv2

from moduld.logger.logger import Logger
from moduld.automation.input import Input
from moduld.automation.screenshot import Screenshot

logger = Logger(level=logging.DEBUG).get_logger()
class Autotools:
    def __init__(self, window_title):
        self.window_title = window_title
        self.screenshot = None
        self.active = True
    
    def take_screenshot(self, crop=(0, 0, 1, 1), max_try_count=5):
        try_count = 0
        while self.active and try_count < max_try_count:
            start_time = time.time()
            try_count += 1
            logger.debug(f"第 {try_count} 次截图。")
            try:
                result = Screenshot.take_screenshot(self.window_title, crop=crop)
                if result:
                    self.screenshot, self.screenshot_pos, self.screenshot_scale_factor = result
                    return result
                else:
                    logger.error("截图失败：没有找到游戏窗口。")
            except Exception as e:
                logger.error(f"截图失败：{e}")
            time_used = time.time() - start_time
            time.sleep(1)
            logger.debug(f"截图成功！用时：{time_used}")
            if time_used > 60:
                raise RuntimeError("截图超时")
    
    def get_image_info(self, image_path):
        # 读图的信息
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is not None:
            logger.debug(f"读取图片({image_path})信息成功！")
            return template.shape[::-1]
        else:
            logger.error("读取图片信息失败！")

    def scale_and_match_template(self, screenshot, template, threshold=None, scale_range=None, mask=None):
        # 模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED, mask=mask)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        logger.debug(f"匹配系数：{max_val}")

        if (math.isinf(max_val) or threshold is None or max_val < threshold) and scale_range is not None:
            for scale in np.arange(scale_range[0], scale_range[1] + 0.0001, 0.05):
                logger.debug(f"缩放 {scale} 倍继续识别。")
                scaled_template = cv2.resize(template, None, fx=scale, fy=scale)
                result = cv2.matchTemplate(screenshot, scaled_template, cv2.TM_CCOEFF_NORMED)
                _, local_max_val, _, local_max_loc = cv2.minMaxLoc(result)

                if local_max_val > max_val:
                    max_val = local_max_val
                    max_loc = local_max_loc
                    logger.debug(f"更新匹配系数：{max_val}")

        return max_val, max_loc

    def find_image_element(self, target, threshold, scale_range=None, relative=False):
        # 寻找某个模板图像，返回它的 左上坐标 和 右下坐标 还有 匹配值
        try:
            # template = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
            template = cv2.imread(target, cv2.IMREAD_UNCHANGED)
            if template is None:
                raise ValueError("读取图片失败")

            if template.shape[2] == 4:  # 检查通道数是否为4（含有透明通道）
                alpha_channel = template[:, :, 3]
                if cv2.minMaxLoc(alpha_channel)[0] == 0:  # 检查是否所有像素值都是最小值（即完全透明）
                    mask = alpha_channel
                else:
                    mask = None
            else:
                mask = None
            template = cv2.imread(target)
            # template = cv2.cvtColor(template, cv2.COLOR_BGRA2RGB)

            # screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2GRAY)
            screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2RGB)
            max_val, max_loc = self.scale_and_match_template(screenshot, template, threshold, scale_range, mask)
            logger.debug(f"目标图片：{target} 相似度：{max_val}")
            if not math.isinf(max_val) and (threshold is None or max_val >= threshold):
                channels, width, height = template.shape[::-1]
                if relative == False:
                    top_left = (
                        max_loc[0] // self.screenshot_scale_factor + self.screenshot_pos[0],
                        max_loc[1] // self.screenshot_scale_factor + self.screenshot_pos[1]
                    )
                else:
                    top_left = (max_loc[0] // self.screenshot_scale_factor,max_loc[1] // self.screenshot_scale_factor)
                bottom_right = (top_left[0] + width // self.screenshot_scale_factor, top_left[1] + height // self.screenshot_scale_factor)
                return top_left, bottom_right, max_val
        except Exception as e:
            logger.error(f"寻找图片出错：{e}")
        logger.debug("没有找到模板图片！")
        return None, None, None
    
    @staticmethod
    def intersected(top_left1, botton_right1, top_left2, botton_right2):
        if top_left1[0] > botton_right2[0] or top_left2[0] > botton_right1[0]:
            return False
        if top_left1[1] > botton_right2[1] or top_left2[1] > botton_right1[1]:
            return False
        return True
    
    @staticmethod
    def count_template_matches(target, template, threshold):
        # 找在这个目标图片里面有几个模板图片
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        match_count = 0
        matches = []
        width, height = template.shape[::-1]
        for top_left in zip(*locations[::-1]):
            flag = True
            for match_top_left in matches:
                botton_right = (top_left[0] + width, top_left[1] + height)
                match_botton_right = (match_top_left[0] + width, match_top_left[1] + height)
                is_intersected = Autotools.intersected(
                    top_left, botton_right, match_top_left, match_botton_right)
                if is_intersected:
                    flag = False
                    break
            if flag == True:
                matches.append(top_left)
                match_count += 1
                logger.debug(f"找到第{match_count}个匹配的模板位置。左上坐标为{top_left}")
        return match_count
    
    def find_image_and_count(self, target, threshold, pixel_bgr=False):
        try:
            template = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
            if template is None:
                raise ValueError("读取图片失败")

            if pixel_bgr:
                screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2RGB)
                bw_map = np.zeros(screenshot.shape[:2], dtype=np.uint8)
                # 遍历每个像素并判断与目标像素的相似性
                bw_map[np.sum((screenshot - pixel_bgr) ** 2, axis=-1) <= 800] = 255
                # bw_map[np.sum(screenshot == pixel_bgr, axis=-1)] = 255
                # cv2.imwrite("tmp/test2.png", bw_map)
                # cv2.imshow("test2", np.array(bw_map))
                # cv2.imshow("test3", np.array(template))
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            else:
                bw_map = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2GRAY)
            return Autotools.count_template_matches(bw_map, template, threshold)
        except Exception as e:
            logger.error(f"寻找图片并计数出错：{e}")
            return None