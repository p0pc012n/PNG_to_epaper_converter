# PNG_to_epaper_converter
Packs PNG images to a split bytearray for epaper grayscale displays that use image overlay

This started with issues encountered using an epaper driver to try to display grayscale images to aa four color grayscale epaper display using a raspberry pi pico 2 w with micropython. I was trying to create my own basic images for a project i had in mind. I kept getting distorted images on the epaper and i finally narrowed it down to how the driver for my display was splitting the packed bytearray to send to the display as two images that are overlayed for the final picture. This is a work in progress.

I created this as a separate script to do the full processing of a four color grayscale image into a split bytearray that can be passed into a function from the display driver class. Currently I am able to pass the two bytearrays into a function onto the fork i pulled from the display driver.

Currently this only supports a 2.9 in four color epaper display in portrait orientation 128px x 296 px.

The PNG file must already be in four color grayscale with RGB values (255,255,255), (103, 103, 103), (23, 23, 23), (0,0,0).
