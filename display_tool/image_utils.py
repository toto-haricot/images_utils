"""This module provides image oriented useful functions such as cropping, zooming and plotting information on a plot
"""

# ---------- IMPORTS ---------------------------------------------------------------------------------

import os
import cv2

# ---------- CENTRAL CROP FUNCTION -------------------------------------------------------------------

def central_crop(image, width_max:int, height_max:int):
    """This function will check is an image already read and given in a numpy array has a width and height in between 
    some limits width_max and height_max. If the image doesn't fit in this range, it is then cropped center on middle

    Args:
        image (np.array): input numpy array
        width_max (int): maximum of pixels / columns in the image
        height_max (int): maximum of pixels / rows in the image

    Returns:
        numpy.array : central cropped version of the image is limits are exceeded or input array otherwise
    """

    width_image, height_image, channels = image.shape

    x_center, y_center = width_image//2, height_image//2


    if (width_image > width_max+1) and (height_image > height_max+1):

        x_margin, y_margin = (width_image - width_max)//2, (height_image - height_max)//2

        cropped_image = image[x_margin:-x_margin, y_margin:-y_margin, :]

        return(cropped_image)


    elif (width_image > width_max+1) and (height_image <= height_max+1):

        x_margin = (width_image - width_max)//2

        cropped_image = image[x_margin:-x_margin,:,:]

        return(cropped_image)

    
    elif (width_image <= width_max+1) and (height_image > height_max+1):

        y_margin = (height_image - height_max)//2

        cropped_image = image[:,y_margin:-y_margin,:]

        return(cropped_image)

    return(image)

# ---------- TEXT ON AN IMAGE ------------------------------------------------------------------------
    
def draw_text_on_image(img, text:str, pos=(20,20), font=cv2.FONT_HERSHEY_DUPLEX, font_scale=2, font_thickness=2,
                       text_color=(0,255,0), text_color_bg=(255,255,255)):
    """Function to write a title on a uniform background on a given image

    Args:
        img (np.array): input image
        text (str): string to write on the image
        pos (tuple, optional): coordinates of the center of the title. Defaults to (20,20)
        font (_type_, optional): open-cv font type. Defaults to cv2.FONT_HERSHEY_DUPLEX
        font_scale (int, optional): open-cv font scale. Defaults to 2
        font_thickness (int, optional): Defaults to 2
        text_color (tuple, optional): color of the text. Defaults to (0,255,0)
        text_color_bg (tuple, optional): color of the background. Defaults to (255,255,255)

    Returns:
        tuple: open-cv size of the title for the given set of parameters
    """
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, (x - text_w, y - text_h), (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (x - text_w//2, y + text_h//2 + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size
            
# ---------- ZOOMING CROP FUNCTION -------------------------------------------------------------------

def zooming_crop(img, crop_style:str='center'):
    """This function returns the crop of an image as a numpy array to create a zoom

    Args:
        img (np.array): the image that we want to crop
        crop_style (str): how do we want to crop the image. Possible values are 'center', 'upper_left', 'upper_right',
                          'bottom_left', 'bottom_right', 'manual', 'automatic'

    Returns:
        np.array: numpy array that plots the cropped image

    """

    input_shape = img.shape

    crop_width = input_shape[1]//5
    crop_height = input_shape[0]//6

    if crop_style == 'center':

        x_center, y_center = input_shape[1]//2, input_shape[0]//2
        start_point = (x_center - crop_width//2, y_center - crop_height//2)
        end_point = (x_center + crop_width//2, y_center + crop_height//2)

        t = input_shape[0]//200

        cropped_image = img[(start_point[1]+t):(end_point[1]-t), (start_point[0]+t):(end_point[0]-t), :]

        cv2.rectangle(img, start_point, end_point, color=(0,0,255), thickness=t)

    cropped_image_rs = cv2.resize(cropped_image, (input_shape[1], input_shape[0]), interpolation=cv2.INTER_AREA)

    return cropped_image_rs
