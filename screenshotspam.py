import time
from PIL import ImageGrab

for i in range(20):
    img = ImageGrab.grab()
    img.save(str(i) + '.png', 'PNG')
    time.sleep(0.5)