""" Functions related to color mixing"""
import cv2
import numpy as np

import ImagePanel

modified_image = ImagePanel.get_image().copy()
mask = np.zeros(modified_image.shape[:2], np.uint8)
mask_color = np.array([0,0,0])

def define_mask(original_color):
    global mask
    global mask_color

    # Verify a location has been picked in the image. If not, do nothing
    if not all([val>0 for val in ImagePanel.get_pick_location()]):
        return
    
    mask_color = original_color.copy()
    
    # Threshold of color to filter for in HSV space 
    mask_hsv_color = cv2.cvtColor(np.uint8([[original_color]]), cv2.COLOR_BGR2HSV).flatten()
    hue_range = 10
    hue_lower_bound = mask_hsv_color[0] - hue_range
    hue_upper_bound = mask_hsv_color[0] + hue_range

    saturation_range = 50
    saturation_lower_bound = mask_hsv_color[1] - saturation_range
    saturation_upper_bound = mask_hsv_color[1] + saturation_range

    value_range = 50
    value_lower_bound = mask_hsv_color[2] - value_range
    value_upper_bound = mask_hsv_color[2] + value_range

    lower_bound = [hue_lower_bound if hue_lower_bound>=0 else 0, saturation_lower_bound if saturation_lower_bound>=0 else 0, value_lower_bound if value_lower_bound>=0 else 0]
    upper_bound = [hue_upper_bound if hue_upper_bound<=179 else 179, saturation_upper_bound if saturation_upper_bound<=255 else 255, value_upper_bound if value_upper_bound<=255 else 255]

    # Filter the image for the given color
    image_hsv = cv2.cvtColor(ImagePanel.get_image(), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_hsv, np.uint8(lower_bound), np.uint8(upper_bound))
    cv2.imshow(winname="mask", mat=cv2.resize(mask, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC))
    cv2.imwrite("outputs/mask.jpg", mask)

def adjust_color(new_color):
    # Verify a location has been picked in the image. If not, do nothing
    if not all([val>0 for val in ImagePanel.get_pick_location()]):
        return
    
    modified_image = ImagePanel.original_image.copy()

    image_hsv = cv2.cvtColor(modified_image.copy(), cv2.COLOR_BGR2HSV)
    new_color_hsv =cv2.cvtColor(np.uint8([[new_color]]), cv2.COLOR_BGR2HSV).flatten()
    
    delta = new_color - mask_color
    modified_image[mask>0] += delta
    modified_image[modified_image < 0] = 0
    modified_image[modified_image>255] = 255

    
#    #new_image = np.array([np.multiply(delta, i) for i in mask.flatten()]).reshape(mask.shape +(3,))
#     cv2.imshow(winname="new_image", mat=modified_image)
    ImagePanel.display_image(modified_image)

def save_cahnges():
    ImagePanel.set_image(modified_image)

