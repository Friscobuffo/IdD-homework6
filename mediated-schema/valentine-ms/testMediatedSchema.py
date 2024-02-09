import os
import json

absPath = os.path.dirname(os.path.abspath(__file__))

groundTrouthPath = os.path.dirname(absPath)+"/ground-truth.json"
with open(groundTrouthPath, 'r') as jsonfile:
    groundTrouth = json.load(jsonfile)

mediatedSchemaPath = absPath + "/mediated-schema.json"
with open(mediatedSchemaPath, 'r') as jsonfile:
    mediatedSchema = json.load(jsonfile)

temp = dict()
for schema in mediatedSchema:
    name = schema.pop("dataset")
    temp[name] = schema
mediatedSchema = temp
temp = dict()
for schema in groundTrouth:
    name = schema.pop("dataset")
    temp[name] = schema
groundTrouth = temp


values = []
for datasetName in mediatedSchema:
    schema = mediatedSchema[datasetName]
    for value in schema.values():
        if value not in values:
            values.append(value)

print(values)
quit()

wrongOnes = 0
totalAttributesChecked = 0
for datasetName in mediatedSchema:
    schema = mediatedSchema[datasetName]
    for attribute in schema:
        totalAttributesChecked += 1
        if schema[attribute] != groundTrouth[datasetName][attribute]:
            wrongOnes += 1
            print("this one is different from ground truth")
            print(f"dataset name: {datasetName}")
            print(f"attribute: {attribute}")
            print(f"ground truth: {groundTrouth[datasetName][attribute]}")
            print(f"given name: {schema[attribute]}")
            print()
print()
print("statistics")
print(f"number of wrong namings: {wrongOnes}")
print(f"number of total attributes: {totalAttributesChecked}")
print(f"precision: {1-(wrongOnes/totalAttributesChecked)}")