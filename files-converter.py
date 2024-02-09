import csv
import json
import shutil
import os
import pandas as pd

def readJsonFile(filePath):
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

directory = "sources-json"
if os.path.exists(directory):
    shutil.rmtree(directory)
os.mkdir(directory)
originalDirectory = "sources"

def csvToJson(csvFilePath, jsonFilePath):
    data = []
    with open(csvFilePath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    with open(jsonFilePath, 'w') as jsonfile:
        jsonfile.write(json.dumps(data, indent=4))

def xlsToJson(xlsFilePath, jsonFilePath):
    df = pd.read_excel(xlsFilePath)
    df.to_json(jsonFilePath, orient='records', indent=4)

files = os.listdir(originalDirectory)
for file in files:
    origin = originalDirectory + "/" + file
    if file.endswith(".json"):
        data = readJsonFile(origin)
        destination = directory + "/" + file
        with open(destination, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        continue
    if file.endswith(".jsonl"):
        data = []
        destination = directory + "/" + file[:-1]
        with open(origin, 'r') as jsonlFile:
            for line in jsonlFile:
                data.append(json.loads(line))
        with open(destination, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)
        continue
    if file.endswith(".csv"):
        destination = directory + "/" + file[:-3] + "json"
        csvToJson(origin, destination)
        continue
    if file.endswith(".xls"):
        destination = directory + "/" + file[:-3] + "json"
        xlsToJson(origin, destination)
        continue
    print(file)