import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
import time
import win32gui, win32ui, win32con
import math
import pydirectinput

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

w = math.floor(0.1 * w)
h = math.floor(0.2 * h)

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

    
# The Prodige ------

# declare needles
unblockable_needle = cv.imread('images/needle.png')

# determine threshholds
unblockable_thresh = 0.4

while True:

    haystack = window_capture()

    cv.imshow('Screen Recording', haystack)

    # check for indicator
    result = cv.matchTemplate(haystack, unblockable_needle, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val >= unblockable_thresh:
        print('Dodge!')
        pydirectinput.keyDown('a')
        pydirectinput.press('space')
        pydirectinput.keyUp('a')

    print(max_val)
    # print('FPS {}'.format(1 / (time() - loop_time)))

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break



print('Done.')
# ----------------------