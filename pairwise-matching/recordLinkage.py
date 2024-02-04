import recordlinkage
from recordlinkage.datasets import load_febrl4
import pandas as pd

json_file_path = '../sources-json/FR_forbes.json'
dfA = pd.read_json(json_file_path)

json_file_path = '../sources-json/slytherin-forbes.com.json'
dfB = pd.read_json(json_file_path)

print(dfA.iloc[1437], dfB.iloc[1446])


# Indexation step
indexer = recordlinkage.Index()
indexer.full()
candidate_links = indexer.index(dfA, dfB)

# Comparison step
compare_cl = recordlinkage.Compare()

compare_cl.exact("Name", "name", label="name")
compare_cl.string("Industry", "industry", threshold=0.85, label="industry")
compare_cl.string("Founded", "founded", threshold=0.85, label="founded")
compare_cl.string("Revenue", "revenue", threshold=0.85, label="revenue")
compare_cl.string("Location", "country", threshold=0.85, label="country")


features = compare_cl.compute(candidate_links, dfA, dfB)

# Classification step
matches = features[features.sum(axis=1) > 3]
print(matches)

