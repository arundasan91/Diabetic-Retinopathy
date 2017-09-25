# Preprocessing Scripts.

## A note about `crop_UWF_image.py`.
The script is primarily used to crop out the standard fundus portions out of UWF retinal images. This seems counter intuitive as UWF images are captured to get the wide field in retinal images in the first place. Cropping it further just makes it similar to a standard fundus image. However, I still created this script to crop square portions out of the UWF image, so that I can train CNN models on multiple sizes of images.

Here's how the algorithm works:
1. Search at the center of the UWF image for the optical disk.
2. Once the optical disk is found, save the location as an anchor point.
3. Crop on all sides, in the given ratio, with the anchor point in the center.

The ratio to crop depends on both `x` and `y` axes. If `crop_ratio_x` and `crop_ratio_y` are both `0.2`, the algorithm will crop 20% of width and height, from the anchor point, - in both `+/- x` and `+/- y` direction.
