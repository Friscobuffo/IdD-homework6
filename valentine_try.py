import os
import pandas as pd
import json
from valentine import valentine_match
from valentine.algorithms import Coma


dataSource = "sources-json"
mappingsSource = "mappings"
files = os.listdir(dataSource)
mappings = os.listdir(mappingsSource)

schemaList = []
schemaNames = []
for file in files:
    filePath = dataSource + "/" + file
    df = pd.read_json(filePath)
    df = df.iloc[:500]
    schemaList.append(df)
    schemaNames.append(file)
totalSchemas = len(schemaList)
totalComparisons = totalSchemas * (totalSchemas-1) / 2
print(f"total schemas: {totalSchemas}")
print(f"total comparisons to do: {totalComparisons}")
matcher = Coma(use_instances=True, java_xmx="1024m")
matches = dict()
for i in range(len(schemaList)-1):
    for j in range(i+1, len(schemaList)):
        print(f"\rcomparison number: {i*j + j}", end="")
        schemaName1 = schemaNames[i]
        schemaName2 = schemaNames[j]
        result = valentine_match(schemaList[i], schemaList[j], matcher, schemaNames[i], schemaNames[j])
        for key in result:
            matches[key] = result
with open("matches", "w") as matchesJson:
    json.dump(matches, matchesJson)