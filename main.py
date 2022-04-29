import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
import win32gui, win32ui, win32con
import math

# TODO: Optimize everything a ton by capturing a smaller part of the screen. First I will expreriment with decreasing width and height
# and see if it remains centered. If it doesn't, offset it with the some stuff that cropped_x and cropped_y does. That should be pretty easy.

# Setup 
window_name = 'For Honor™'
hwnd = win32gui.FindWindow(None, window_name)

window_rect = win32gui.GetWindowRect(hwnd)
w = window_rect[2] - window_rect[0] 
h = window_rect[3] - window_rect[1] 

border_pixels = 8
titlebar_pixels = 30
w = w - (border_pixels * 2)
h = h - titlebar_pixels - border_pixels


cropped_x = border_pixels
cropped_y = titlebar_pixels

# reducing window size ------

cropped_x += math.floor(w / 2)
cropped_y += math.floor(h / 2)

w = math.floor(0.4 * w)
h = math.floor(0.5 * h)

cropped_x -= math.floor(w / 2)
cropped_y -= math.floor(h / 2)

# ---------------------------


# screenshot functions
def list_open_windows():
    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print (hex(hwnd), win32gui.GetWindowText( hwnd ))

    win32gui.EnumWindows( winEnumHandler, None )

def window_capture():
    

    # get the image window data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)

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


list_open_windows()
print('Done.')