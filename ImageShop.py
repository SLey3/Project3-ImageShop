# File: ImageShop.py

"""
This program is the starter file for the ImageShop application, which
implements the "Load" and "Flip Vertical" buttons.
"""

from filechooser import choose_input_file
from pgl import GWindow, GImage, GRect
from button import GButton
from GrayscaleImage import create_grayscale_image, luminance
from itertools import accumulate

# Constants

GWINDOW_WIDTH = 900
GWINDOW_HEIGHT = 500
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

# The ImageShop application

def image_shop():
    def add_button(label, action):
        """Adds a button to the region on the left side of the window."""
        x = BUTTON_MARGIN
        y = gw.next_button_y
        button = GButton(label, action)
        button.set_size(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        gw.next_button_y += BUTTON_HEIGHT + BUTTON_MARGIN

    def set_image(image):
        """Sets image as the current image after removing the old one."""
        if gw.current_image is not None:
            gw.remove(gw.current_image)
        gw.current_image = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.get_width()) / 2
        y = (gw.get_height() - image.get_height()) / 2
        gw.add(image, x, y)

    def load_button_action():
        """Callback function for the Load button"""
        filename = choose_input_file()
        if filename != "":
            set_image(GImage(filename))

    def clear_action():
        """Callback function for the Clear button"""
        if gw.current_image is not None:
            set_image(clear(gw.current_image))

    def flip_vertical_action():
        """Callback function for the Flip Vertical button"""
        if gw.current_image is not None:
            set_image(flip_vertical(gw.current_image))

    def flip_horizontal_action():
        """Callback function for the Flip Horizontal button"""
        if gw.current_image is not None:
            set_image(flip_horizontal(gw.current_image))

    def rotate_left_action():
        if gw.current_image is not None:
            set_image(rotate_left(gw.current_image))
    
    def rotate_right_action():
        if gw.current_image is not None:
            set_image(rotate_right(gw.current_image))

    def grayscale_action():
        if gw.current_image is not None:
            set_image(create_grayscale_image(gw.current_image))
    
    def green_screen_action():
        gimage = choose_input_file()
        if gw.current_image is not None and gimage != "":
            set_image(green_screen(gw.current_image, GImage(gimage)))

    def equalize_action():
        if gw.current_image is not None:
            set_image(equalize(gw.current_image))

    def color_negative_action():
        if gw.current_image is not None:
            set_image(color_negative(gw.current_image))

    def correct_red_eye_effect_action():
        if gw.current_image is not None:
            set_image(correct_red_eye_effect(gw.current_image))

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    button_area = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)
    button_area.set_filled(True)
    button_area.set_color(BUTTON_BACKGROUND)
    gw.add(button_area)
    gw.next_button_y = BUTTON_MARGIN
    gw.current_image = None
    add_button("Load", load_button_action)
    add_button("Clear", clear_action)
    add_button("Flip Vertical", flip_vertical_action)
    add_button("Flip Horizontal", flip_horizontal_action)
    add_button("Rotate Left", rotate_left_action)
    add_button("Rotate Right", rotate_right_action)
    add_button("Grayscale", grayscale_action)
    add_button("Green Screen", green_screen_action)
    add_button("Equalize", equalize_action)
    add_button("Color Negative", color_negative_action)
    add_button("Red Eye Corrector", correct_red_eye_effect_action)

def clear(image):
    """clears canvas"""
    array = image.get_pixel_array()
    height = len(array)
    width = len(array[0])

    new_array = [[0 for j in range(width)] for i in range(height)]

    return GImage(new_array)

def flip_vertical(image):
    """Creates a new GImage by flipping image vertically."""
    array = image.get_pixel_array()
    return GImage(array[::-1])

def flip_horizontal(image):
    """Creates a GImage by flipping image horizontally"""
    array = image.get_pixel_array()
    height = len(array)
    width = len(array[0])

    for i in range(height):
        for j in range(width // 2):
            old_pos = array[i][j]
            new_pos = array[i][width-j-1]
            
            o_r = GImage.get_red(old_pos)
            o_g = GImage.get_green(old_pos)
            o_b = GImage.get_blue(old_pos)

            n_r = GImage.get_red(new_pos)
            n_g = GImage.get_green(new_pos)
            n_b = GImage.get_blue(new_pos)

            array[i][j] = GImage.create_rgb_pixel(n_r, n_g, n_b)
            array[i][width-j-1] = GImage.create_rgb_pixel(o_r, o_g, o_b)
    
    return GImage(array)

def rotate_left(image):
    """Rotates Image to the left (90 degrees)"""
    array = image.get_pixel_array()

    array = [list(row) for row in zip(*array)][::-1]

    return GImage(array)

def rotate_right(image):
    """Rotates Image to the right (270 degrees)"""
    array = image.get_pixel_array()

    for _ in range(2 + 1):
        array = [list(row) for row in zip(*array)][::-1]

    return GImage(array)

def green_screen(image, gimage):
    """Applies a image w/ green screen to overlay image"""
    # background
    overlay_array = image.get_pixel_array()
    oheight = len(overlay_array)
    owidth = len(overlay_array[0])
    # image with green screen
    g_array = gimage.get_pixel_array()
    gheight = len(g_array)
    gwidth = len(g_array[0])

    for ni in range(oheight):
        for nj in range(owidth):
            opixel = g_array[ni][nj]
            r = GImage.get_red(opixel)
            g = GImage.get_green(opixel)
            b = GImage.get_blue(opixel)

            try:
                greenIntensity = g / ((r + b) / 2)
            except ZeroDivisionError:
                greenIntensity = g

            if greenIntensity < 1.5:
                overlay_array[ni][nj] = opixel
    return GImage(overlay_array)
 
def pixel_counter(h, w):
    count = 0
    for i in range(h):
        for j in range(w):
            count += 1
    return count

def create_img_histogram(array, h, w):
    img_histogram = []
    # iterate through intensity values
    for k in range(0, 256):
        count1 = 0
        for i in range(h):
            for j in range(w):
                if luminance(array[i][j]) == k:
                    count1 += 1
        img_histogram.append(count1)
    return img_histogram


def equalize(image):
    """Equalizes a grayscale image through histogram equalization"""
    array = image.get_pixel_array()
    height = len(array)
    width = len(array[0])

    P = pixel_counter(height, width)

    img_histogram = create_img_histogram(array, height, width)

    cumulative_histogram = list(accumulate(img_histogram))

    for i in range(height):
        for j in range(width):
            pixel = array[i][j]
            L = luminance(pixel)

            nl = round((255 * cumulative_histogram[L]) / P)

            array[i][j] = GImage.create_rgb_pixel(nl, nl, nl)

    return GImage(array)

def color_negative(image):
    """Inverts Image colors"""
    array = image.get_pixel_array()
    height = len(array)
    width = len(array[0])

    for i in range(height):
        for j in range(width):
            old_pixel = array[i][j]

            r = GImage.get_red(old_pixel)
            g = GImage.get_green(old_pixel)
            b = GImage.get_blue(old_pixel)

            new_pixel = GImage.create_rgb_pixel(255 - r, 255 - g, 255 - b)

            array[i][j] = new_pixel

    return GImage(array)

def correct_red_eye_effect(image):
    """Corrects red  eye effect if present in image"""
    array = image.get_pixel_array()
    height = len(array)
    width = len(array[0])
    for i in range(height):
        for j in range(width):
            pixel = array[i][j]
            r = GImage.get_red(pixel)
            g = GImage.get_green(pixel)
            b = GImage.get_blue(pixel)

            try:
                redIntensity = r / ((g + b) / 2)
            except ZeroDivisionError:
                redIntensity = r

            if redIntensity > 1.5:
                rr = max(g ,b)
                array[i][j] = GImage.create_rgb_pixel(rr, g, b)
    return GImage(array)

# Startup code  

if __name__ == "__main__":
    image_shop()
