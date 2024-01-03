"""
Title: LSNR
Description: Generic SNR Calculation
Author: Anıl Karaca
Date: 29.12.2023

Example Usage:
python snr.py --directory_path "/path/to/images" --output_excel_file "/path/to/output.xlsx"
"""

import cv2
import numpy as np
import os
import pandas as pd
import argparse

def calculate_snr(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    signal_mean = np.mean(img)
    noise_std = np.std(img)
    snr = signal_mean / noise_std if noise_std != 0 else float('inf')
    return snr

def process_images_in_directory(directory):
    data = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            snr = calculate_snr(image_path)
            data.append({'Filename': filename, 'SNR': snr})
    return pd.DataFrame(data)

def write_results_to_excel(dataframe, output_file):
    sorted_dataframe = dataframe.sort_values(by='Filename')
    sorted_dataframe.to_excel(output_file, index=False)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generic SNR Calculation")
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
