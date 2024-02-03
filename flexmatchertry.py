import flexmatcher
import pandas as pd
import os
import json
import pickle

dataSource = "sources-json"
mappingsSource = "mappings"
files = os.listdir(dataSource)
mappings = os.listdir(mappingsSource)

# training
schemaList = []
mappingList = []
for file in files:
    filePath = dataSource + "/" + file
    if file in mappings:
        mappingPath = mappingsSource + "/" + file
        with open(mappingPath, 'r') as file:
            mapping = json.load(file)
        df = pd.read_json(filePath)
        for column in list(df):
            df[column] = df[column].astype(str)
        schemaList.append(df)
        mappingList.append(mapping)
# fm = flexmatcher.FlexMatcher(schemaList, mappingList, sample_size=1000)
# fm.train()
# pickle.dump(fm, open("model-flexmatcher", 'wb'))

with open('model-flexmatcher', 'rb') as pickle_file:
    fm = pickle.load(pickle_file)
df = pd.read_json("sources-json/slytherin-forbes.com.json")
predicted_mapping = fm.make_prediction(df)
for key in predicted_mapping:
    print(key, predicted_mapping[key])