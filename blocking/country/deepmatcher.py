import deepmatcher as dm
import os
import json
import pandas as pd
import torch
from itertools import product

json_path = os.path.join('blocking', 'country', 'blocks_data.json')
csv_path = os.path.join('blocking', 'country', 'Portugal.csv')
with open(json_path) as file:
    data = json.load(file)

df = pd.DataFrame(data["Portugal"])

combinations = list(product(df.to_dict(orient='records'), repeat=2))

#Estraggo gli attributi per ogni combinazione ed assegno il nome left_* e right_*
result = []
for left,right in combinations:
    left_dict = {'left_' + k: v for k, v in left.items()}
    right_dict = {'right_' + k: v for k, v in right.items()}
    result.append({**left_dict, **right_dict})

result_df = pd.DataFrame(result)
result_df['label'] = 0 # Aggiungo la colonna label fillata con valori = 0

result_df.to_csv(csv_path)
