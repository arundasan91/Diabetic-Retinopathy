#encoding: utf-8
# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

# This script will intelligently crop UWF images to standard fundus size.
# To do this, the script first find the optical disk from the fundus photograph
# and then crop out a portion out of it, with optical disk as the anchor point.

def crop_image_by_ratio(image, crop_ratio_x, crop_ratio_y, show_img=False):
    """
    Cropping images based on height and width ratios from both sides.
    """
    (h,w) = image.shape[:2]
    h_range_min = h*crop_ratio_y
    h_range_max = h*(1-crop_ratio_y)
    w_range_min = w*crop_ratio_x
    w_range_max = w*(1-crop_ratio_x)
    cropped = image[h_range_min:h_range_max, w_range_min:w_range_max]
    if show_img:
        plt.imshow(cropped, cmap='gray')
        plt.show()
    return cropped, w, h, w_range_min, h_range_min

def find_optic_disk(fundus_image_path, show_image=False, crop_ratio_x=0.1, crop_ratio_y=0.1, show_circle=False, radius=11, circle_thickness=2, save_fig=False):
    # Read image and crop the sides
    # Cropping the sides by 10 percent (or more) will help to
    # remove the alien objects in UWF images.
    # Might have to tweak this number in the future.
    print fundus_image_path
    fundus_orig = cv2.imread(fundus_image_path)
    image, w, h, w_range_min, h_range_min = crop_image_by_ratio(fundus_orig, crop_ratio_x, crop_ratio_y)
    # Make a copy of the image.
    orig = image.copy()
    # Convert to gray scale and apply Gaussian Blur.
    # Image is blurred to reduce the frequency of maximum brightness points.
    # Gaussian blur radius can be tuned later.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (radius,radius), 0)
    # Find the location of maximum brightness.
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # Find the corresponding maximum brightness location in the original fundus image
    orig_max_loc = (int(maxLoc[0] + w_range_min), int(maxLoc[1] + h_range_min))
    # Draw a circle around the maximum brightness location.
    if show_circle:
        cv2.circle(fundus_orig, orig_max_loc, radius, (255, 0, 0), circle_thickness)
    if save_fig:
        # Add this later.
        #cv2.imwrite()
        pass
    if show_image:
        plt.imshow(cv2.cvtColor(fundus_orig, cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        return fundus_orig, w, h, orig_max_loc

def crop_image_from_point_by_ratio(image, crop_ratio_x, crop_ratio_y, anchor, show_image=False):
    """
    Crop images on all sides, according to height and width ratio, from an anchor point.
    It crops crop_ratio_x percentage in both sides in X direction from the anchor point and
    crop_ratio_y percentage in both sides in the Y direction.
    """
    (h,w) = image.shape[:2]
    a_w, a_h = anchor
    if h*crop_ratio_y > w*crop_ratio_x:
        crop_factor = h*crop_ratio_y
    else:
        crop_factor = w*crop_ratio_x
    h_range_min = a_h - crop_factor
    h_range_max = a_h + crop_factor
    w_range_min = a_w - crop_factor
    w_range_max = a_w + crop_factor
    #print h_range_min, h_range_max, w_range_min, w_range_max
    cropped = image[h_range_min:h_range_max, w_range_min:w_range_max]
    if show_image:
        plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        plt.show()
    return cropped

def crop_UWF_intelligent(fundus_image_path, show_image=False, save_fig=False, crop_ratio_x=0.2, crop_ratio_y=0.2, radius=11, circle_thickness=2):
    """
    A wrapper function to extract standard fundus part from UWF images.
    """
    img, w, h, loc = find_optic_disk(fundus_image_path, show_image=False, save_fig=False, crop_ratio_x=crop_ratio_x, crop_ratio_y=crop_ratio_y, radius=radius, circle_thickness=circle_thickness)
    cropped = crop_image_from_point_by_ratio(img, crop_ratio_x, crop_ratio_y, loc, show_image)
    if save_fig:
        # Do it later
        pass
    else:
        return cropped
'''        
Example:
image_path = '/Users/arundas/Development/DiabeticRetinopathy/Datasets/retina_images/ARMD-0058.jpg'
_ = crop_UWF_intelligent(image_path, crop_ratio_x=0.25, crop_ratio_y=0.25, show_image=True, radius=11)
'''
