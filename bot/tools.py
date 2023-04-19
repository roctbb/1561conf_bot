import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import cv2

def get_mask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray[gray < 128] = 0
    gray[gray >= 128] = 255

    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)

    return gray

def count_red(path):
    # load a frame as int16 array to avoid overflow etc. when subtracting
    img = cv2.resize(cv2.imread(path), (1024, 1024))

    mask = get_mask(img.copy())

    img = img.astype(np.int16)

    img_b = img[:, :, 0]
    img_g = img[:, :, 1]
    img_r = img[:, :, 2]

    img_b[mask == 0] = 0
    img_g[mask == 0] = 0
    img_r[mask == 0] = 0

    # for a red stripe, the red component should be much bigger than the rest
    res_br = img_r - img_b
    res_gr = img_r - img_g
    res = np.maximum(res_br, res_gr)
    res[res < 64] = 0
    res[res >= 64] = 255
    res = res.astype(np.uint8)  # convert back to uint8 for findContours etc.


    kernel = np.ones((2, 2), np.uint8)
    res = cv2.erode(res, kernel, iterations=1)


    kernel = np.ones((21, 21), np.uint8)
    res = cv2.dilate(res, kernel, iterations=1)

    ret, thresh = cv2.threshold(res, 250, 1, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # gives the correct output of 5
    return len(contours)


def qr_decode(path):
    try:
        return str(decode(Image.open(path))[0].data).rstrip("'").lstrip('b\'')
    except:
        return None
