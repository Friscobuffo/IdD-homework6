import json
import os

def readJsonFile(filePath):
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
TABLES_PATH = ABS_PATH + "/tables"
filesNames = os.listdir(TABLES_PATH)
for fileName in filesNames:
    filePath = TABLES_PATH + "/" + fileName
    jsonDict = readJsonFile(filePath)