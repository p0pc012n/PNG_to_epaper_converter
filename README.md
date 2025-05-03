# PNG_to_epaper_converter
Packs PNG images to a split bytearray for epaper grayscale displays that use image overlay

Components:
1. Raspberry Pi Pico 2 W
2. Waveshare 2.9 inch E-Paper E-Ink Four (4) Color Grayscale Display Module for Raspberry PI Pico, 296x128, SPI

I had problems with writing grayscale images to the display. I found a lot of different methods online that were helpful but couldn't get them to fully work because they were written for different display sizes, lcd displays, or black and white. I could not find clear enough documentation for the look up tables that are in the offiical driver for the pico. I needed to display the images in landscape mode but could never get rid of the artifacting. I could never figure out the image rotation the waveshare driver is performing and encountered the same issue in trying to figure out how the waveshare driver was unpacking the bytearray to split into two images.

Waveshare has a wiki for the Pico e-Paper 2.9 displays at: https://www.waveshare.com/wiki/Pico-ePaper-2.9

After using the wiki for reference, I ultimately inserted my own function into the waveshare driver and perfomed all image processing on my pc to just use the final prepared bytearrays directly on the pico. 
This python script is the final product of that image pre-processing.

Because i couldn't consisitently get the Landscape class to work on waveshare driver I focused on the portrait orientation. I still needed the landscape orientation though.
I initially triend inkscape but realized soon into the project, that vector graphics were not the solution. I settled on drawing my images in GIMP with the image size set exactly to my epaper display size in the landscape orientation. I set my grid to 1 pixel width. I had a lot of the completed images in .svg so i imported those in GIMP to their own layer to use for tracing, and anything that deviated I just freehanded on the 1 pixel width grids.
When I was ready, I rotated my image to portraint orientation and made any corrections.

GIMP Settings:
1. 1 grid pixel width
2. image size exactly the same pixel width and height as the epaper display
3. image orienation to match the orientation class that is more completed in the original waveshare driver
4. Draw only in 4 color grayscale. I tried matching the same hex codes from the Waveshare wiki.
5. Choose to export as a single image or layers individually
6. Export to .png, no scaling, 8bit RGB or 8bit 4 color Gray

GIMP Notes: I think i may have used 8bit 4 color gray export to success. Most of my latest exports were 8bit RGB and when i used the same 4 color gray hex codes from the Waveshare Wiki my exported RGB values were black (0,0,0), dark gray (23, 23, 23), light gray (103, 103, 103), and white (255, 255, 255).

My PNG_to_epaper_converter reads through the .png top to bottom, left to right pixel by pixel. It's currently set up for pixels to be the exact RGB values as above. I hope to find time to come back and account for more values to reduce the upfront manual workload.

This was my first time doing anything with image processing and bits, so i am still not fullly familiar with fundamentals or the theory, but I did finally figure out how to process the image exactly to the specifications that the waveshare display needs it for 4 color grayscale.

The waveshare display needs to split the images to two then it overlays them. I do not understand all the technical points, other than waveshare wiki refers to a x24 registry and x26 registry.
To convert a .png to a grayscale compatible bytearrays, you do not pack 8 pixels into a bit. Instead you are packing 16 pixels into a bit. If the wiki is clear on this then I just completely missed it.

My PNG_to_epaper_converter reads the RGB one one pixel such as (255, 255, 255) and converts it to the bit value 00. From my understanding usually you do this to 4 total pixels then convert the string to a byte. The waveshare display needs it split. So the PNG_to_epaper_converter will iterate through pixels and convert each RGB value to a bit 00 adn then split it to two respective lists, one for x24, and the other for x26. The first bit goes to x24 and the second bit goes to x26. PNG_to_epaper_converter will continue doing this until there are 8 bits to convert to a byte (checked with len() % 8). Then the completed bytes are added to a x24 bytearray and x26 bytearray. This process is continued until the end.
Originally i had whtie RGB (255, 255, 255) assigned to bit 11 and black RGB (0, 0, 0) to 00 but that was resulting in an inverted image to what i had created in GIMP. I altered the '0' and '1' values for all four colors in the script.

Compatibility notes:
This is currently set for exactly a 296 pixel by 128 pixel display in portrait orienation. I hope to come back and make this more modular. The image class from pillow in PNG_to_epaper_converter is set to read from the center of the pixel so i used the float values 0.5, 295.5, etc for pixel coordinates. At the time it seemd to be the most sure way to process the correct pixel. Previous methods resulted in scaled images or lost values until i finally landed on the current method.

The resulting x24 and x26 bytearrays can be read directly into a function i wrote in my fork of the waveshare driver for the 2.9 display.
waveshare 2.9 fork: https://github.com/p0pc012n/pico_epaper_image/blob/main/python/Pico_ePaper-2.9.py

I found that using the base functions in the micropyton framebuffer module, you able to before different writing, text, shapes, etc. and add the functions to the framebuffer before sending it to the display, but i could not have any success with any kind of grayscale image generation. This was one of the largest reasons that pushed me to processing the images outside of the pico and just writing one image to the display as needed.
I was able to further use the resulting bytearray in a GUI-like application for anther project where i used bytearray manipulation to "update" images. It's still peforming a full display update, but i am able to have fewer bytearrays that can then be combined as needed. You can view that here: https://github.com/p0pc012n/rv-open-systems-monitor
