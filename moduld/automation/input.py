from moduld.logger.logger import Logger
import logging
import pyautogui
import time

logger = Logger(level=logging.DEBUG).get_logger()
class Input:
    pyautogui.FAILSAFE = False

    @staticmethod
    def mouse_click(x, y):
        try:
            pyautogui.click(x, y)
            logger.debug(f"鼠标点击 ({x}, {y})")
        except Exception as e:
            logger.error(f"鼠标点击出错：{e}")

    @staticmethod
    def mouse_down(x, y):
        try:
            pyautogui.mouseDown(x, y)
            logger.debug(f"鼠标按下 ({x}, {y})")
        except Exception as e:
            logger.error(f"鼠标按下出错：{e}")

    @staticmethod
    def mouse_up():
        try:
            pyautogui.mouseUp()
            logger.debug("鼠标释放")
        except Exception as e:
            logger.error(f"鼠标释放出错：{e}")

    @staticmethod
    def mouse_move(x, y):
        try:
            pyautogui.moveTo(x, y)
            logger.debug(f"鼠标移动 ({x}, {y})")
        except Exception as e:
            logger.error(f"鼠标移动出错：{e}")

    @staticmethod
    def mouse_scroll(count, direction=-1):
        for i in range(count):
            pyautogui.scroll(direction)
        logger.debug(f"滚轮滚动 { count * direction } 次")

    @staticmethod
    def press_key(key, wait_time=0.2):
        try:
            pyautogui.keyDown(key)
            time.sleep(wait_time)
            pyautogui.keyUp(key)
            logger.debug(f"键盘按下 {key}")
        except Exception as e:
            logger.debug(f"键盘按下 {key} 出错：{e}")

    @staticmethod
    def press_mouse(wait_time=0.2):
        try:
            pyautogui.mouseDown()
            time.sleep(wait_time)
            pyautogui.mouseUp()
            logger.debug(f"按下鼠标左键")
        except Exception as e:
            logger.debug(f"按下鼠标左键出错：{e}")