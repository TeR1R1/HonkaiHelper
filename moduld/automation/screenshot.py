from PIL import Image
import numpy as np
import pyautogui
import win32gui

class Screenshot:
    @staticmethod
    def is_application_fullscreen(window):
        # 检测 window 是不是全屏
        screen_width, screen_height = pyautogui.size()
        return (window.width, window.height) == (screen_width, screen_height)

    @staticmethod
    def get_window_real_resolution(window):
        # 获取 window 的宽和高
        left, top, right, bottom = win32gui.GetClientRect(window._hWnd)
        return right - left, bottom - top

    @staticmethod
    def get_window_region(window):
        if Screenshot.is_application_fullscreen(window):
            return (window.left, window.top, window.width, window.height)
        else:
            real_width, real_height = Screenshot.get_window_real_resolution(window)
            other_border = (window.width - real_width) // 2
            up_border = window.height - real_height - other_border
            return (window.left + other_border, window.top + up_border, window.width - other_border - other_border, window.height - up_border - other_border)

    @staticmethod
    def get_window(title):
        # 用 title 获取窗口
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return window
        return False

    @staticmethod
    def take_screenshot(title, crop=(0, 0, 1, 1)):
        # 截图，crop 是比例
        window = Screenshot.get_window(title)
        if window:
            left, top, width, height = Screenshot.get_window_region(window)

            screenshot = pyautogui.screenshot(region=(
                int(left + width * crop[0]),
                int(top + height * crop[1]),
                int(width * crop[2]),
                int(height * crop[3])
            ))

            real_width, _ = Screenshot.get_window_real_resolution(window)
            if real_width > 1920:
                screenshot_scale_factor = 1920 / real_width
                screenshot = screenshot.resize((int(1920 * crop[2]), int(1080 * crop[3])))
            else:
                screenshot_scale_factor = 1

            screenshot_pos = (
                int(left + width * crop[0]),
                int(top + height * crop[1]),
                int(width * crop[2] * screenshot_scale_factor),
                int(height * crop[3] * screenshot_scale_factor)
            )

            return screenshot, screenshot_pos, screenshot_scale_factor

        return False
    
    @staticmethod
    def get_all_windows():
        # 获取所有窗口句柄和标题
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hwnd, win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
        
    @staticmethod
    def set_before_title(title):
        # 置以 title 为标题的窗口于顶层
        hwnd = win32gui.FindWindow(None, 'QQ')
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
        else: return False
        
    @staticmethod
    def show_screenshot(screenshot): 
        # 展示图像
        Image.fromarray(np.array(screenshot)).show()
    
    @staticmethod
    def save_screenshot(screenshot, path):
        # 保存图像到 path
        Image.fromarray(np.array(screenshot)).save(path)