#!/usr/bin/python3
import os
import cv2
import numpy as np

import ColorPallet
import editor_modes.ColorMixer as ColorMixer

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "Lightroom_1", "512A0266.jpg")
original_image = cv2.resize(cv2.imread(IMAGE_PATH), (0, 0), fx=0.15, fy=0.15, interpolation=cv2.INTER_CUBIC)
image = original_image.copy()

pick_location = (-1,-1)

def open():
    """ Initialize the image window. """
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_event)
    reload_image()

def reload_image():
    """ Resets the loaded image to it's original state """
    global image 
    image = original_image.copy()
    cv2.imshow(winname="image", mat=image)

def click_event(event, x, y, flags, params):
    """ When the image is clicked, mark the location on the image """
    if event == cv2.EVENT_LBUTTONDOWN:
        # Set the pick location
        global pick_location

        save_image_changes()
        
        # Add the pick marker to the image
        pick_location = (x,y)
        display_image(original_image.copy())

        # Update ColorPallet to have selected color
        ColorPallet.update_hsv_track_bars(image[y,x])

def get_image():
    return image

def display_image(new_image=get_image().copy()):
    global image
    image = new_image.copy()
    image_marked = new_image.copy()
    cv2.circle(
        img=image_marked, center=pick_location, radius=5, color=(0, 0, 255), thickness=2
    )
    cv2.imshow(winname="image", mat=image_marked)

def get_pick_location():
    """ Getter function for pick location """
    return pick_location

def save_image_changes():
    global original_image 
    original_image = image.copy()
    cv2.imshow(winname="image", mat=image)



if __name__ == "__main__":
    open()

    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
