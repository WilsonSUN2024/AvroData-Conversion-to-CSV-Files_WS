# -*- coding = utf-8 -*-
# @Software : PyCharm
# Original Source: 
https://support.empatica.com/hc/en-us/articles/17405877853981-How-to-access-Avro-files-with-Python


from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os

## Define the location of the Avro file and output folder.
avro_file_path = "C:/Users/Weihao/Desktop/AVRODATA1/1-1-PAR0030_1759422932.avro"
output_dir = "C:/Users/Weihao/Desktop/AVRODATA1/output/"

## Read Avro file
reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
schema = json.loads(reader.meta.get("avro.schema").decode("utf-8"))
data = next(reader)

## Uncomment the below 2 lines to print the Avro schema
# print(schema)
# print(" ")

## Uncomment the below 2 lines to export the entire content into a JSON file
# with open(os.path.join(output_dir, "content.json"), "w") as f:
#     json.dump(data, f, indent=4)

## Export sensors data to csv files
avro_version = (
    (data["schemaVersion"]["major"]),
    (data["schemaVersion"]["minor"]),
    (data["schemaVersion"]["patch"]),
)

# Accelerometer
acc = data["rawData"]["accelerometer"]
timestamp = [
    round(acc["timestampStart"] + i * (1e6 / acc["samplingFrequency"]))
    for i in range(len(acc["x"]))
]
# Convert ADC counts in g
if avro_version < (6, 5, 0):
    delta_physical = acc["imuParams"]["physicalMax"] - acc["imuParams"]["physicalMin"]
    delta_digital = acc["imuParams"]["digitalMax"] - acc["imuParams"]["digitalMin"]
    x_g = [val * delta_physical / delta_digital for val in acc["x"]]
    y_g = [val * delta_physical / delta_digital for val in acc["y"]]
    z_g = [val * delta_physical / delta_digital for val in acc["z"]]
else:
    conversion_factor = acc["imuParams"]["conversionFactor"]
    x_g = [val * conversion_factor for val in acc["x"]]
    y_g = [val * conversion_factor for val in acc["y"]]
    z_g = [val * conversion_factor for val in acc["z"]]
with open(os.path.join(output_dir, "accelerometer.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "x", "y", "z"])
    writer.writerows([[ts, x, y, z] for ts, x, y, z in zip(timestamp, x_g, y_g, z_g)])

# Eda
eda = data["rawData"]["eda"]
timestamp = [
    round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
    for i in range(len(eda["values"]))
]
with open(os.path.join(output_dir, "eda.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "eda"])
    writer.writerows([[ts, eda] for ts, eda in zip(timestamp, eda["values"])])

# Temperature
tmp = data["rawData"]["temperature"]
timestamp = [
    round(tmp["timestampStart"] + i * (1e6 / tmp["samplingFrequency"]))
    for i in range(len(tmp["values"]))
]
with open(os.path.join(output_dir, "temperature.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "temperature"])
    writer.writerows([[ts, tmp] for ts, tmp in zip(timestamp, tmp["values"])])

# Tags
tags = data["rawData"]["tags"]
with open(os.path.join(output_dir, "tags.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["tags_timestamp"])
    writer.writerows([[tag] for tag in tags["tagsTimeMicros"]])

# BVP
bvp = data["rawData"]["bvp"]
timestamp = [
    round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
    for i in range(len(bvp["values"]))
]
with open(os.path.join(output_dir, "bvp.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "bvp"])
    writer.writerows([[ts, bvp] for ts, bvp in zip(timestamp, bvp["values"])])

# Systolic peaks
sps = data["rawData"]["systolicPeaks"]
with open(os.path.join(output_dir, "systolic_peaks.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["systolic_peak_timestamp"])
    writer.writerows([[sp] for sp in sps["peaksTimeNanos"]])

# Steps
steps = data["rawData"]["steps"]
timestamp = [
    round(steps["timestampStart"] + i * (1e6 / steps["samplingFrequency"]))
    for i in range(len(steps["values"]))
]
with open(os.path.join(output_dir, "steps.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "steps"])
    writer.writerows([[ts, step] for ts, step in zip(timestamp, steps["values"])])
