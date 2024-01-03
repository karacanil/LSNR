"""
Title: LSNR
Description: Generate basic image for sanity check
Author: Anıl Karaca
Date: 29.12.2023
"""

from PIL import Image
import numpy as np

# Assume 'array' is your 2D numpy array
# Normalize the array to ensure it's in the 0-255 range if it's not already

array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 4, 4, 5, 5, 5, 4, 4, 0],
    [0, 0, 4, 4, 5, 5, 5, 4, 4, 0],
    [0, 0, 4, 4, 5, 5, 5, 4, 4, 0],
    [0, 0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

array = np.clip(array, 0, 255)  # Assuming the array is already scaled between 0 and 255
array = array.astype('uint8')   # Convert to unsigned byte

# Create an image from the array
img = Image.fromarray(array, 'L')  # 'L' mode is for grayscale

# Save the image
img.save('generated_image.png')

loaded_image = Image.open("generated_image.png")


width, height = loaded_image.size
for x in range(height):
    for y in range(width):
        pixel_value = loaded_image.getpixel((y, x))
        print(pixel_value, end=" ")
    print("")