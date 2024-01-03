"""
Title: LSNR
Description: Extract .xml Bounding Boxes to JSON and YAML format
Author: Anıl Karaca
Date: 29.12.2023

Example Usage:
python bb.py --directory_path "/path/to/xml" --output_json_file "/path/to/coordinates.json" --output_yaml_file "/path/to/coordinates.yaml"
"""

import xml.etree.ElementTree as ET
import json
import yaml
import os
import argparse


def parse_xml_and_extract_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extracting width and height
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    data = {'width': width, 'height': height, 'objects': []}

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')

        if bndbox is not None:
            coordinates = {
                'xmin': int(bndbox.find('xmin').text),
                'ymin': int(bndbox.find('ymin').text),
                'xmax': int(bndbox.find('xmax').text),
                'ymax': int(bndbox.find('ymax').text)
            }
            data['objects'].append(coordinates)

    return data

def process_xml_files_in_directory(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(directory, filename)
            print(xml_file_path)
            data[filename] = parse_xml_and_extract_data(xml_file_path)
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def save_to_yaml(data, output_file):
    with open(output_file, 'w') as file:
        yaml.dump(data, file)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract .xml Bounding Boxes to JSON and YAML format")
    parser.add_argument("--directory_path", type=str, required=True, help="Path to the folder containing XML files")
    parser.add_argument("--output_json_file", type=str, required=True, help="Path for the output JSON file")
    parser.add_argument("--output_yaml_file", type=str, required=True, help="Path for the output YAML file")

    # Parse arguments
    args = parser.parse_args()

    # Process XML files and save results
    bounding_box_data = process_xml_files_in_directory(args.directory_path)
    save_to_json(bounding_box_data, args.output_json_file)
    save_to_yaml(bounding_box_data, args.output_yaml_file)

    print(f"Results written to {args.output_json_file} and {args.output_yaml_file}")

if __name__ == "__main__":
    main()