import cv2 as cv
from cv2 import threshold
import numpy as np

haystack_img = cv.imread('images/noattack.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('images/needle.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

threshold = 0.8
if max_val >= threshold:
    print('Dodge!')
else:
    print('Do nothing.')