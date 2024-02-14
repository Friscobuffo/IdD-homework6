import os
import json

absPath = os.path.dirname(os.path.abspath(__file__))

groundTrouthPath = os.path.dirname(absPath)+"/ground-truth.json"
with open(groundTrouthPath, 'r') as jsonfile:
    groundTruth = json.load(jsonfile)

mediatedSchemaPath = absPath + "/mediated-schema.json"
with open(mediatedSchemaPath, 'r') as jsonfile:
    mediatedSchema = json.load(jsonfile)

temp = dict()
for schema in mediatedSchema:
    name = schema.pop("dataset")
    temp[name] = schema
mediatedSchema = temp
temp = dict()
for schema in groundTruth:
    name = schema.pop("dataset")
    temp[name] = schema
groundTruth = temp
print(f"size of ground truth: {len(groundTruth)}")
print(f"size of mediated schema: {len(mediatedSchema)}")


values = []
for datasetName in mediatedSchema:
    schema = mediatedSchema[datasetName]
    for value in schema.values():
        if value not in values:
            values.append(value)

print(values)

wrongOnes = 0
totalAttributesChecked = 0
for datasetName in mediatedSchema:
    schema = mediatedSchema[datasetName]
    for attribute in schema:
        totalAttributesChecked += 1
        if schema[attribute] != groundTruth[datasetName][attribute]:
            wrongOnes += 1
            print("this one is different from ground truth")
            print(f"dataset name: {datasetName}")
            print(f"attribute: {attribute}")
            print(f"ground truth: {groundTruth[datasetName][attribute]}")
            print(f"given name: {schema[attribute]}")
            print()
print()
print("statistics")
print(f"number of wrong namings: {wrongOnes}")
print(f"number of total attributes: {totalAttributesChecked}")
print(f"precision: {1-(wrongOnes/totalAttributesChecked)}")

sumRecall = 0
n = 0
for value in values:
    n += 1
    total = 0
    for datasetName in mediatedSchema:
        dataset = groundTruth[datasetName]
        for oldKey in dataset:
            newKey = dataset[oldKey]
            if newKey == value: total += 1
    goods = 0
    for datasetName in mediatedSchema:
        dataset = mediatedSchema[datasetName]
        for oldKey in dataset:
            newKey = dataset[oldKey]
            if newKey == groundTruth[datasetName][oldKey] and newKey == value:
                goods += 1
    sumRecall += (goods/total)

print(sumRecall/n)