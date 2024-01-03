"""
Title: LSNR
Description: Local SNR Calculation for Target Detection 
Author: Anıl Karaca
Date: 29.12.2023

Example Usage:
python snr_bb.py --directory_path "/path/to/images" --output_excel_file "/path/to/output.xlsx"
"""

import numpy as np
from PIL import Image
import json
import os
import pandas as pd
import argparse

class ImageDetails:
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self.objects = []

    def add_object(self, xmin, ymin, xmax, ymax):
        self.objects.append({'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

def get_image_details_from_json(json_file, image_name):
    with open(json_file, 'r') as file:
        data = json.load(file)

    json_key = image_name.replace('.png', '.xml')

    if json_key in data:
        image_data = data[json_key]
        det = ImageDetails(image_data['width'], image_data['height'])

        for obj in image_data['objects']:
            det.add_object(obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax'])

        return det
    else:
        return None

def calculate_mean_std(pixel_list):
    return np.mean(pixel_list), np.std(pixel_list)

def calculate_snr(image, image_details):
    if not image_details.objects:
        return None

    snrs = []
    for obj in image_details.objects:
        detection_pixel_list = []
        neighbor_pixel_list = []

        for i in range(obj['xmin'], obj['xmax']):
            for j in range(obj['ymin'], obj['ymax']):
                index = j * image_details.Width + i
                detection_pixel_list.append(image[index])

        # Define the neighborhood area
        N = max(obj['ymax'] - obj['ymin'], obj['xmax'] - obj['xmin']) * 2
        topLeftX = max((obj['xmin'] + obj['xmax']) // 2 - N // 2, 0)
        topLeftY = max((obj['ymin'] + obj['ymax']) // 2 - N // 2, 0)
        bottomRightX = min(topLeftX + N, image_details.Width)
        bottomRightY = min(topLeftY + N, image_details.Height)

        for i in range(topLeftX, bottomRightX):
            for j in range(topLeftY, bottomRightY):
                if obj['xmin'] <= i < obj['xmax'] and obj['ymin'] <= j < obj['ymax']:
                    continue
                if j < image_details.Height:
                    index = j * image_details.Width + i
                    neighbor_pixel_list.append(image[index])

        mean_detection, std_detection = calculate_mean_std(detection_pixel_list)
        mean_neighbor, std_neighbor = calculate_mean_std(neighbor_pixel_list)
        snr = abs(mean_detection - mean_neighbor) / std_neighbor
        snrs.append(snr)

    return np.mean(snrs) if snrs else None

def process_images_in_directory(directory):
    data = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            loaded_image = Image.open(image_path)

            if loaded_image.mode != 'L':
                loaded_image = loaded_image.convert('L')

            image = np.array(loaded_image).flatten()
            json_file_path = "./coordinates.json"
            image_details = get_image_details_from_json(json_file_path, filename)

            snr = calculate_snr(image, image_details)
            if snr is not None:
                data.append({'Filename': filename, 'SNR': round(snr, 2)})

    return pd.DataFrame(data)

def write_results_to_excel(dataframe, output_file):
    sorted_dataframe = dataframe.sort_values(by='Filename')
    sorted_dataframe.to_excel(output_file, index=False)

# Main execution
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Local SNR Calculation for Target Detection")
    parser.add_argument("--directory_path", type=str, required=True, help="Path to the directory containing images")
    parser.add_argument("--output_excel_file", type=str, required=True, help="Path for the output Excel file")

    # Parse arguments
    args = parser.parse_args()

    # Process images and write results
    snr_results = process_images_in_directory(args.directory_path)
    write_results_to_excel(snr_results, args.output_excel_file)
    print(f"Results written to {args.output_excel_file}")

if __name__ == "__main__":
    main()
