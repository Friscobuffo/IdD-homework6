import os
import json

absPath = os.path.dirname(os.path.abspath(__file__))

mediatedSchemaPath = absPath + "/valentine-ms/mediated-schema.json"
with open(mediatedSchemaPath, 'r') as jsonfile:
    mediatedSchema = json.load(jsonfile)

temp = dict()
for schema in mediatedSchema:
    name = schema.pop("dataset")
    temp[name] = schema
mediatedSchema = temp

dataSource = absPath + "/valentine-ms/sources-json"
files = os.listdir(dataSource)

finalAttr = []
for schema in mediatedSchema.values():
    for value in schema.values():
        if value not in finalAttr:
            finalAttr.append(value)

finalTable = []
for file in files:
    filePath = dataSource + "/" + file
    with open(filePath, 'r') as jsonfile:
        entries = json.load(jsonfile)
    for entry in entries:
        temp = dict()
        
        for attr in mediatedSchema[file]:
            temp[mediatedSchema[file][attr]] = entry[attr]
        
        for attr in finalAttr:
            if attr not in temp:
                temp[attr] = ""

        finalTable.append(temp)

finalTablePath = absPath + "/final-table.json"
if os.path.exists(finalTablePath):
    os.remove(finalTablePath)
with open(finalTablePath, "w") as json_file:
    json.dump(finalTable, json_file, indent=4)