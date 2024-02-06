import os
import recordlinkage
from recordlinkage.datasets import load_febrl4
import pandas as pd
import json

absPath = os.path.dirname(os.path.abspath(__file__))
json_file_path = absPath + '/../mediated-schema/final-table.json'
dfA = pd.read_json(json_file_path)

# Indexation step
indexer = recordlinkage.Index()
indexer.block("country")
candidate_links = indexer.index(dfA, dfA)

# Comparison step
compare_cl = recordlinkage.Compare()

compare_cl.string("company_name", "company_name", threshold=0.85, label="company_name")
compare_cl.string("country", "country", threshold=0.85, label="country")
#compare_cl.string("sector", "sector", threshold=0.85, label="sector")
compare_cl.string("revenue", "revenue", threshold=0.85, label="revenue")
compare_cl.string("founding_year", "founding_year", threshold=0.85, label="founding_year")

features = compare_cl.compute(candidate_links, dfA, dfA)

# Classification step
matches = features[features.sum(axis=1) > 3]

#cleaned_matches = matches.drop_duplicates(subset=['company_name', 'country'])


for couple in matches.index:
    if couple[0] >= couple[1]:
        matches.drop(couple, inplace=True)
        
print(matches)

################### sperimentale ###################
        
finalTablePath = absPath + "/../mediated-schema/final-table.json"
with open(finalTablePath, 'r') as jsonfile:
    finalTable = json.load(jsonfile)
print(len(finalTable))

index = matches.index
delete_index = []
print(len(index))
for couple in index:
    for key in finalTable[0]:
        if finalTable[couple[0]][key] == "" and finalTable[couple[1]][key] != "":
            finalTable[couple[0]][key] = finalTable[couple[1]][key]
    delete_index.append(couple[1])

fixedTable = []
for i in range(0, len(finalTable)):
    if i not in delete_index:
        fixedTable.append(finalTable[i])


print(len(fixedTable))

fixedFinalTablePath = absPath + "/../mediated-schema/fixed-final-table.json"
if os.path.exists(fixedFinalTablePath):
    os.remove(fixedFinalTablePath)
with open(fixedFinalTablePath, "w") as json_file:
    json.dump(fixedTable, json_file, indent=4)





