import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
import win32gui, win32ui, win32con

def window_capture():
    w = 1920 
    h = 1080 

    # hwnd = win32gui.FindWindow(None, windowname)
    hwnd = None

    # get the image window data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

    # save the screenshot
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h,  w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # get rid of alpha channel
    img = img[...,:3]

    img = np.ascontiguousarray(img)

    return img

    


loop_time = time()
while True:

    screenshot = window_capture()

    cv.imshow('Screen Recording', screenshot)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')