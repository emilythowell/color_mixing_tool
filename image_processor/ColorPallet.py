#!/usr/bin/python3
import cv2
import numpy as np

import editor_modes.ColorMixer as ColorMixer

WINDOW_NAME = "color_pallet"
color = np.zeros((300, 512, 3), np.uint8)

def open(open_color=[0,0,0]):
    global color

    cv2.namedWindow(WINDOW_NAME)

    # cv2.createTrackbar("Red", WINDOW_NAME, open_color[2], 255, (lambda red: _update_color_bgr([-1,-1,red])))
    # cv2.createTrackbar("Green", WINDOW_NAME, open_color[1], 255, (lambda green: _update_color_bgr([-1,green,-1])))
    # cv2.createTrackbar("Blue", WINDOW_NAME, open_color[0], 255, (lambda blue: _update_color_bgr([blue,-1,-1])))

    hsv = cv2.cvtColor(np.uint8([[open_color]]), cv2.COLOR_BGR2HSV).flatten()
    cv2.createTrackbar("Hue", WINDOW_NAME, hsv[0], 179, (lambda h: _update_color_hsv(hue=h)))
    cv2.createTrackbar("Saturation", WINDOW_NAME, hsv[1], 255, (lambda s: _update_color_hsv(sat=s)))
    cv2.createTrackbar("Luminosity", WINDOW_NAME, hsv[2], 255, (lambda l: _update_color_hsv(lum=l)))

    _update_color_bgr(open_color)

def _update_color_hsv(hue=-1, sat=-1, lum=-1):
    """Updates the color displayed when the Red, Green, or Blue scale bars are adjusted

    Args:
        new_color (np.array): Color value array
    """
    global color
            
    if hue < 0:
        hue = cv2.getTrackbarPos("Hue", WINDOW_NAME)

    if sat < 0:
        sat = cv2.getTrackbarPos("Saturation", WINDOW_NAME)

    if lum < 0:
        lum = cv2.getTrackbarPos("Luminosity", WINDOW_NAME)

    new_color = [hue, sat, lum]
    color[:] = cv2.cvtColor(np.uint8([[new_color]]), cv2.COLOR_HSV2BGR).flatten()
    cv2.imshow(winname=WINDOW_NAME, mat=color)
    ColorMixer.adjust_color(color[0,0])

def _update_color_bgr(new_color, color_conversion=None):
    """Updates the color displayed when the scale bars are adjusted

    Args:
        new_color (np.array): Color value array
        color_conversion (_type_, optional): If the color given IS NOT in brg, provide the appropriate conversion code
    """
    global color
    
    for index, val in enumerate(new_color):
        if val < 0:
            new_color[index] = cv2.cvtColor(np.uint8([[new_color]]), color_conversion).flatten()

    if color_conversion is not None:
        new_color = cv2.cvtColor(np.uint8([[new_color]]), color_conversion).flatten()

    color[:] = new_color
    cv2.imshow(winname=WINDOW_NAME, mat=color)

def update_track_bars(new_color):
    update_bgr_track_bars(new_color)
    update_hsv_track_bars(new_color)

def update_bgr_track_bars(new_color):
    hsv = cv2.cvtColor(np.uint8([[new_color]]), cv2.COLOR_BGR2HSV).flatten()
    cv2.setTrackbarPos("Red", WINDOW_NAME, new_color[2])
    cv2.setTrackbarPos("Green", WINDOW_NAME, new_color[1])
    cv2.setTrackbarPos("Blue", WINDOW_NAME, new_color[0])

def update_hsv_track_bars(new_color):
    ColorMixer.define_mask(new_color)
    hsv = cv2.cvtColor(np.uint8([[new_color]]), cv2.COLOR_BGR2HSV).flatten()
    cv2.setTrackbarPos("Hue", WINDOW_NAME, hsv[0])
    cv2.setTrackbarPos("Saturation", WINDOW_NAME, hsv[1])
    cv2.setTrackbarPos("Luminosity", WINDOW_NAME, hsv[2])

if __name__ == "__main__":
    open()

    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
