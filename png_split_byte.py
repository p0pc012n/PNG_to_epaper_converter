from PIL import Image
import os

# === file path config ===
parent_dir = os.path.dirname(__file__)
file_name = "your_file_name.png"  # Replace with your image filename
file_path = os.path.join(parent_dir, file_name)
base_name = file_name[:-5]

# === Load the image as RGB ===
img = Image.open(file_path).convert("RGB")
pixel_list = []
# pixel_map = os.path.join(parent_dir, "lg_pixel_map.txt")

# with open(pixel_map, "a") as file:
y_counter = 0.5
while y_counter <= 295.5:
    x_counter = 0.5
    while x_counter <= 127.5:
        r, g, b = img.getpixel((x_counter, y_counter))
        # file.write(f"({r}, {g}, {b}), ")
        pixel_rgb = (r, g, b)
        pixel_list.append(pixel_rgb)
        x_counter += 1
    # file.write("\n")
    y_counter += 1

rgb_counter = 0
x24_list = [""]
x26_list = [""]
rgb_index = 0
for pix in pixel_list:
    rgb_counter += 1
    if pix == (255, 255, 255):
        x24_list[rgb_index] += "0"
        x26_list[rgb_index] += "0"
    elif pix == (0, 0, 0):
        x24_list[rgb_index] += "1"
        x26_list[rgb_index] += "1"
    elif pix == (23, 23, 23):
        x24_list[rgb_index] += "0"
        x26_list[rgb_index] += "1"
    elif pix == (103, 103, 103):
        x24_list[rgb_index] += "1"
        x26_list[rgb_index] += "0"
    if rgb_counter % 8 == 0:
        x24_list.append("")
        x26_list.append("")
        rgb_index += 1

x24_list = [pix for pix in x24_list if pix != ""]
x26_list = [pix for pix in x26_list if pix != ""]

# x24_file = os.path.join(parent_dir, "lg_x24_map.txt")
# x26_file = os.path.join(parent_dir, "lg_x26_map.txt")

# with open(x24_file, "w") as file:
#    file.write(f"rgb_map ={x24_list}")
x24_image_data = bytearray(int(b, 2) for b in x24_list)

# with open(x26_file, "w") as file:
#    file.write(f"rgb_map ={x26_list}")
x26_image_data = bytearray(int(b, 2) for b in x26_list)


check_x24_byte = []
# for byte in x24_image_data:
#     if byte in check_x24_byte:
#         pass
#     else:
#         check_x24_byte.append(byte)
# print(check_x24_byte)
x24_bit_file = os.path.join(parent_dir, "x24_bit_color.py")

check_x26_byte = []
# for byte in x26_image_data:
#     if byte in check_x26_byte:
#         pass
#     else:
#         check_x26_byte.append(byte)
# print(check_x26_byte)
x26_bit_file = os.path.join(parent_dir, "x26_bit_color.py")


with open(x24_bit_file, "w") as f:
    f.write("x24_image_data = bytearray([\n")
    for i, byte in enumerate(x24_image_data):
        f.write(f"    0x{byte:02x},\n")
    f.write("])\n")

with open(x26_bit_file, "w") as f:
    f.write("x26_image_data = bytearray([\n")
    for i, byte in enumerate(x26_image_data):
        f.write(f"    0x{byte:02x},\n")
    f.write("])\n")
