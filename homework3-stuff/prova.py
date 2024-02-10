import json
import os
import pandas as pd
from valentine import valentine_match
from valentine.algorithms import Coma

def readJsonFile(filePath):
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
TABLES_PATH = ABS_PATH + "/tables"
filesNames = os.listdir(TABLES_PATH)
tables = dict()
for fileName in filesNames:
    filePath = TABLES_PATH + "/" + fileName
    jsonDict = readJsonFile(filePath)
    tableName = jsonDict["id"]
    cells = jsonDict["cells"]
    rows = jsonDict["maxDimensions"]["row"]
    columns = jsonDict["maxDimensions"]["column"] + 1
    headers = ["" for _ in range(columns)]
    table = [["" for _ in range(columns)] for _ in range(rows)]
    for cell in cells:
        if cell["isHeader"]:
            headers[cell["Coordinates"]["column"]] = cell["cleanedText"]
        else:
            row = cell["Coordinates"]["row"]-1
            column = cell["Coordinates"]["column"]
            table[row][column] = cell["cleanedText"]   
    tableDataframe = pd.DataFrame(table, columns=headers)
    tables[tableName] = tableDataframe




PROCESSED_FINAL_TABLE_PATH = ABS_PATH + "/processed-final-table2.json"
finalTable = pd.read_json(PROCESSED_FINAL_TABLE_PATH)
finalTable = finalTable.iloc[:100]


matcher = Coma(use_instances=True, java_xmx="2048m")
matches = dict()
for i, tableName in enumerate(tables):
    table = tables[tableName]
    print(f"{i} - {tableName}")
    result = valentine_match(finalTable, table.iloc[:100], matcher)
    for key in result:
        score = result[key]
        key = (("final-table", key[0][1]), (tableName, key[1][1]))
        matches[key] = score

for match in matches:
    # print(match)
    score = matches[match]
    if match[0][1]=="company_name" and score>0.3:
        print(match, score)

quit()

sets = []
for key in matches:
    dataset0 = key[0]
    dataset1 = key[1]
    combined = set()
    combined.add(dataset0)
    combined.add(dataset1)
    j = 0
    for s in sets:
        if dataset0 in s:
            temp = sets.pop(j)
            combined = combined.union(temp)
        j += 1
    j = 0
    for s in sets:
        if dataset0 in s:
            temp = sets.pop(j)
            combined = combined.union(temp)
        j += 1
    sets.append(combined)

PROCESSED_MATCHES_DIRECTORY = ABS_PATH + "/processed-matches"
if os.path.exists(PROCESSED_MATCHES_DIRECTORY):
    shutil.rmtree(PROCESSED_MATCHES_DIRECTORY)
os.mkdir(PROCESSED_MATCHES_DIRECTORY)
for i, s in enumerate(sets):
    fileName = "matches"+str(i)+".txt"
    filePath = PROCESSED_MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'w') as f:
        for elem in s:
            f.write(str(elem) + '\n')

labelsMediatedSchema = []
for s in sets:
    print(s)
    print("what name do you want to give to this set of attibutes?")
    name = input()
    print()
    labelsMediatedSchema.append(name)

SOURCES_DIRECTORY = ABS_PATH + "/sources-json"
files = os.listdir(SOURCES_DIRECTORY)
schemas = []
for file in files:
    filePath = SOURCES_DIRECTORY + "/" + file
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)[0]
    for key in data:
        label = None
        for i, s in enumerate(sets):
            for elem in s:
                dataset = elem[0]
                column = elem[1]
                if dataset != file: continue
                if key != column: continue
                label = labelsMediatedSchema[i]
                break
            if label: break
        if not label:
            print(f"{key} from {file} needs a label, input wanted label:")
            label = input()
        data[key] = label
    data["dataset"] = file
    schemas.append(data)

mediatedSchemaPath = ABS_PATH + "/mediated-schema.json"
if os.path.exists(mediatedSchemaPath):
    os.remove(mediatedSchemaPath)
with open(mediatedSchemaPath, "w") as json_file:
    json.dump(schemas, json_file, indent=4)