import json
import os
import pandas as pd
from valentine import valentine_match
from valentine.algorithms import Coma
import pickle
import re
import shutil
from time import time

start = time()

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
            text = cell["cleanedText"]
            pattern = r"\d{2}x\d{2}px"
            text = re.sub(pattern, '', text)
            text = text.strip()
            table[row][column] = text  
    tableDataframe = pd.DataFrame(table, columns=headers)
    tables[tableName] = tableDataframe

PROCESSED_FINAL_TABLE_PATH = ABS_PATH + "/processed-final-table2.json"
finalTable = pd.read_json(PROCESSED_FINAL_TABLE_PATH)
finalTable = finalTable.iloc[:200]
oldMediatedSchemaHeader = set(finalTable.columns.tolist())
newMediatedSchemaHeader = set(finalTable.columns.tolist())
finalTable.rename(columns={'country': 'country_headquarters'}, inplace=True)

MATCHES_PATH = ABS_PATH + "/matches"
if os.path.exists(MATCHES_PATH):
    with open(MATCHES_PATH, 'rb') as pickleFile:
        matches = pickle.load(pickleFile)
else:
    matcher = Coma(use_instances=True, java_xmx="2048m")
    matches = dict()
    for i, tableName in enumerate(tables):
        table = tables[tableName]
        print(f"{i} - {tableName}")
        result = valentine_match(finalTable, table.iloc[:200], matcher)
        for key in result:
            score = result[key]
            key = (("final-table", key[0][1]), (tableName, key[1][1]))
            matches[key] = score    
    with open(MATCHES_PATH, "wb") as file:
        pickle.dump(matches, file)

candidateTables = set()
for match in matches:
    score = matches[match]
    if match[0][1]=="company_name" and score>0.3:
        tableName = match[1][0]
        candidateTables.add(tableName)
print(f"number of candidate tables: {len(candidateTables)}")

processedMatches = dict()
for match in matches:
    tableName = match[1][0]
    if tableName not in candidateTables: continue
    score = matches[match]
    if score < 0.3: continue
    originalColumn = match[0][1]
    toColumn = match[1][1]
    if tableName not in processedMatches:
        processedMatches[tableName] = [(originalColumn, toColumn, score)]
    else:
        processedMatches[tableName].append((originalColumn, toColumn, score))

for tableName in processedMatches:
    print(tableName)
    print(processedMatches[tableName])
    print()

headerFinalTable = finalTable.columns.tolist()
print()

OUTPUT_PATH = ABS_PATH + "/output"
if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)

print(len(processedMatches))

totalNewEntries = 0
for number,tableName in enumerate(processedMatches):
    table = tables[tableName]
    oldHeader = table.columns.tolist()
    print(tableName)
    print("old header", end = "")
    print(oldHeader)
    newHeader = table.columns.tolist()
    for i, columnName in enumerate(oldHeader):
        for originalColumn, toColumn, _ in processedMatches[tableName]:
            if toColumn == columnName:
                newHeader[i] = originalColumn
    if "country_headquarters" in newHeader:
        position = newHeader.index("country_headquarters")
        newHeader[position] = "country"
    print("new header", end = "")
    print(newHeader)
    print("\ngood matches:")
    for columnName in oldHeader:
        for match in matches:
            score = matches[match]
            if match[1] == (tableName, columnName) and score>0.3 and match[0][1] != "company_name":
                print(match[0][1], " - ", match[1][1], score)
    table.columns = newHeader
    print()
    newMediatedSchemaHeader.update(newHeader)
    print(table.iloc[:5])
    tablePath = OUTPUT_PATH+"/"+str(number)+'.json'
    print(tablePath)
    table.to_json(tablePath, orient='records', indent=4)
    print("\n\n\n")
    totalNewEntries += len(table)

print(f"total new entries: {totalNewEntries}")
print()
print(f"old mediated schema: {len(oldMediatedSchemaHeader)}")
print(oldMediatedSchemaHeader)
print()
print(f"new mediated schema: {len(newMediatedSchemaHeader)}")
print(newMediatedSchemaHeader)

print(f"time: {time() - start}")
