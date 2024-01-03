# Target-Based Local SNR Calculation

This Target-Based Local SNR Calculation is used to analyze small target detection datasets, such as [SIRST](https://github.com/YimianDai/sirst), [SIRSTv2](https://github.com/YimianDai/open-sirst-v2) and [IRSTD-1k](https://github.com/RuiZhang97/ISNet). This value indicates the dimness of the targets.

### Generic SNR
```
python snr.py --directory_path "/path/to/images" --output_excel_file "/path/to/output.xlsx"
```

### Target-Based Local SNR
```
python snr_bb.py --directory_path "/path/to/images" --output_excel_file "/path/to/output.xlsx"
```

### Convert Images to 8-bit Grayscale
```
python convert.py --input_folder "/path/to/tiff" --output_folder "/path/to/output"
```

### Extract .xml Bounding Boxes to JSON and YAML format
```
python bb.py --directory_path "/path/to/xml" --output_json_file "/path/to/coordinates.json" --output_yaml_file "/path/to/coordinates.yaml"
```

