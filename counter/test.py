
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

def count():

    #load a frame as int16 array to avoid overflow etc. when subtracting
    img = cv2.resize(cv2.imread("8b8c3490-8404-4b16-bce8-9e7df4bbb559.jpg"), (1024, 1024))

    cv2.imshow('image', img)
    cv2.waitKey(0)

    mask = get_mask(img.copy())
    cv2.imshow('image', mask)
    cv2.waitKey(0)

    img = img.astype(np.int16)

    #separating into blue, green and red channels
    img_b = img[:, :, 0]
    img_g = img[:, :, 1]
    img_r = img[:, :, 2]

    img_b[mask == 0] = 0
    img_g[mask == 0] = 0
    img_r[mask == 0] = 0

    #for a red stripe, the red component should be much bigger than the rest
    res_br = img_r - img_b
    res_gr = img_r - img_g
    res = np.maximum(res_br, res_gr)
    res[res < 64] = 0
    res[res >= 64] = 255
    res = res.astype(np.uint8)  #convert back to uint8 for findContours etc.

    cv2.imshow('image', res)
    cv2.waitKey(0)

    kernel = np.ones((3, 3), np.uint8)
    res = cv2.erode(res, kernel, iterations=1)

    cv2.imshow('image', res)
    cv2.waitKey(0)

    kernel = np.ones((20, 20), np.uint8)
    res = cv2.dilate(res, kernel, iterations=1)

    cv2.imshow('image', res)
    cv2.waitKey(0)

    ret, thresh = cv2.threshold(res, 250, 1, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #gives the correct output of 5
    print(len(contours))

def qr_decode():


    print(str(decode(Image.open('IMG_8266.jpg'))[0].data))

qr_decode()
count()