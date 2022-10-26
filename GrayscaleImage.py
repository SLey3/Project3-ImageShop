# File: GrayscaleImage.py

"""
This program displays an image together with its grayscale equivalent.
"""

from pgl import GWindow, GImage

# Constants

GWINDOW_WIDTH = 800
GWINDOW_HEIGHT = 600
IMAGE_FILENAME = "images/Vermeer-Milkmaid.png"
IMAGE_SEP = 50

# Main program

def grayscale_image():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    image = GImage(IMAGE_FILENAME)
    gw.add(image, (gw.get_width() - IMAGE_SEP) / 2 - image.get_width(),
                  (gw.get_height() - image.get_height()) / 2)
    grayscale = create_grayscale_image(image)
    gw.add(grayscale, (gw.get_width() + IMAGE_SEP) / 2,
                      (gw.get_height() - image.get_height()) / 2)

def create_grayscale_image(image):
    """
    Creates a grayscale image based on the luminance of each pixel
    """
    array = image.get_pixel_array()
    height = len(array)
    width = len(array[0])
    for i in range(height):
        for j in range(width):
            gray = luminance(array[i][j])
            array[i][j] = GImage.create_rgb_pixel(gray, gray, gray)
    return GImage(array)

def luminance(pixel):
    """
    Returns the luminance of a pixel, which indicates its subjective
    brightness.  This implementation uses the NTSC formula.
    """
    r = GImage.get_red(pixel)
    g = GImage.get_green(pixel)
    b = GImage.get_blue(pixel)
    return round(0.299 * r + 0.587 * g + 0.114 * b)

# Startup code

if __name__ == "__main__":
    grayscale_image()
