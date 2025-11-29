# AvroData-Conversion-to-CSV-Files_WS
## 2. Empatica Avro Data Extraction

### Overview
This script extracts sensor data from **Empatica Avro files** and converts them into CSV files. The supported sensors include:

- Accelerometer
- EDA (Electrodermal Activity)
- Temperature
- BVP (Blood Volume Pulse)
- Systolic Peaks
- Steps
- Tags

### Requirements
- Python 3.x
- `avro-python3` (`pip install avro-python3`)

### Usage
1. Set your Avro file path and output directory in the script:
    ```python
    avro_file_path = "path/to/your/file.avro"
    output_dir = "path/to/output/folder/"
    ```
2. Run the script:
    ```bash
    python extract_avro_to_csv.py
    ```
3. CSV files for each sensor will be saved in the output folder.

---
