import csv
import json
import shutil
import os

def readCsvFile(filePath):
    data = []
    with open(filePath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

# filePath = 'example.csv'
# csvData = readCsvFile(filePath)
# for row in csvData:
#     print(row)


def readJsonFile(filePath):
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

# filePath = 'example.json'
# jsonData = readJsonFile(filePath)
# print(jsonData)

directory = "sources-json"
if os.path.exists(directory):
    shutil.rmtree(directory)

os.mkdir(directory)
originalDirectory = "sources"

def csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)

    with open(json_file_path, 'w') as jsonfile:
        jsonfile.write(json.dumps(data, indent=4))

files = os.listdir(originalDirectory)
for file in files:
    origin = originalDirectory + "/" + file
    if file.endswith(".json"):
        # # shutil.copy(origin, directory)
        data = readJsonFile(origin)
        destination = directory + "/" + file
        print(destination)
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
        fileJson = directory+"/"+file[:-3]+"json"
        csv_to_json(origin, fileJson)
        continue
    print(file)
