"""
Title: LSNR
Description: Convert Current Images to 8-bits Grayscale Images
Author: Anıl Karaca
Date: 29.12.2023

Example Usage:
python convert.py --input_folder "/path/to/tiff" --output_folder "/path/to/output"
"""

import os
import numpy as np
from PIL import Image
import argparse


def convert_to_8bit_grayscale(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all TIFF files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".tiff"):
            file_path = os.path.join(input_folder, filename)
            with Image.open(file_path) as img:
                # Convert the image to a numpy array for processing
                img_array = np.array(img)

                # Check if the image has more than one channel (e.g., RGB)
                if len(img_array.shape) > 2:
                    # Convert to grayscale by taking the average of the channels
                    img_array = img_array.mean(axis=2)

                # Normalize the image only if min and max values are different
                if img_array.min() != img_array.max():
                    normalized_img_array = (img_array - img_array.min()) * (255 / (img_array.max() - img_array.min()))
                    img_array = normalized_img_array

                # Convert the array to uint8 type
                img_array = img_array.astype('uint8')

                # Convert back to PIL image in 8-bit grayscale
                img_8bit = Image.fromarray(img_array, 'L')

                # Save the image as PNG in the output folder
                output_path = os.path.join(output_folder, filename.replace(".tiff", ".png"))
                img_8bit.save(output_path)
                print(f"Converted and saved: {output_path}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert TIFF images to 8-bit grayscale PNG")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to the folder containing TIFF images")
    parser.add_argument("--output_folder", type=str, required=True, help="Path to the folder to save converted PNG images")

    # Parse arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    convert_to_8bit_grayscale(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
