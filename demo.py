import win32gui
import win32con
import pyautogui
    
def getTitleNumber(winTitle):
    winNumberList = []
    win32gui.EnumWindows(
        lambda hWnd, param: param.append(hWnd),
        winNumberList
    )
    
    for winNumber in winNumberList:
        if win32gui.GetWindowText(winNumber) == winTitle:
            return winNumber

def setActive(honkai3):
    if win32gui.IsIconic(honkai3):
        win32gui.ShowWindow(honkai3, win32con.SW_RESTORE)
    
    win32gui.SetForegroundWindow(honkai3)
    win32gui.SetWindowPos(
        honkai3,
        win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE
    )
    
if __name__ == '__main__':
    honkai3 = getTitleNumber('崩坏3')
    setActive(honkai3)
