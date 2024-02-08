import os
import recordlinkage
import pandas as pd
import unicodedata as uc
import Levenshtein

def normalize_text(stringa):
    return uc.normalize('NFKD', stringa).encode('ascii', 'ignore').decode('utf-8')

def match(dfA, dfB, min_score = 3):
    # Indexation step
    indexer = recordlinkage.Index()
    indexer.full()
    candidate_links = indexer.index(dfA, dfB)

    # Comparison step
    compare_cl = recordlinkage.Compare()

    compare_cl.string("company_name", "company_name", threshold=0.85, label="company_name")
    compare_cl.string("country", "country", threshold=0.85, label="country")
    compare_cl.string("sector", "sector", threshold=0.85, label="sector")
    compare_cl.string("revenue", "revenue", threshold=0.85, label="revenue")
    compare_cl.string("founding_year", "founding_year", threshold=0.85, label="founding_year")

    features = compare_cl.compute(candidate_links, dfA, dfB)
    # Classification step
    matches = features[features.sum(axis=1) > min_score]
    for couple in matches.index:
        if couple[0] >= couple[1]:
            matches.drop(couple, inplace=True)
    
    return matches

def normalizedDistance(str1, str2):
    # Calcola la distanza di Levenshtein
    dist = Levenshtein.distance(str1, str2)

    # Normalizza utilizzando la normalizzazione min-max
    maxLen = max(len(str1), len(str2))
    normalizedDist = dist / maxLen

    return round(normalizedDist,2)


def personal_match(dfA, dfB, keys, threshold = 0.1, min_score = 3):
    scores = dict()
    for indexA, rowA in dfA.iterrows():
        for indexB, rowB in dfB.iterrows():
            score = dict()
            for key in keys:
                if rowA[key] == "" and rowB[key] == "":
                    score[key] = 1
                else:
                    score[key] = normalizedDistance(rowA[key], rowB[key])
            scores[(indexA,indexB)] = score

    scores = {k: v for k, v in scores.items() if k[0] < k[1]}

    matches = {k: v for k, v in scores.items() if sum(v.values()) < threshold * min_score}

    print("from %d got %d matches" %(len(dfA), len(matches)))
    return len(matches)
            


if __name__ == "__main__":    
    absPath = os.path.dirname(os.path.abspath(__file__))

    tot_matches = 0
    dataSource = absPath + "/custom-blocks"
    files = os.listdir(dataSource)
    for file in files:
        if file == ".json":
            continue
        print(file)
        json_file_path = absPath + '/custom-blocks/' + file
        dfA = pd.read_json(json_file_path)
        dfA = dfA.map(lambda x: normalize_text(x) if isinstance(x, str) else x)
        dfA = dfA.astype(str)
        tot_matches += personal_match(dfA, dfA, ["company_name"], 0.1, 1)
    
    print(tot_matches)
        


################### sperimentale ###################
        
# finalTablePath = absPath + "/../mediated-schema/final-table.json"
# with open(finalTablePath, 'r') as jsonfile:
#     finalTable = json.load(jsonfile)
# print(len(finalTable))

# index = matches.index
# delete_index = []
# print(len(index))
# for couple in index:
#     for key in finalTable[0]:
#         if finalTable[couple[0]][key] == "" and finalTable[couple[1]][key] != "":
#             finalTable[couple[0]][key] = finalTable[couple[1]][key]
#     delete_index.append(couple[1])

# fixedTable = []
# for i in range(0, len(finalTable)):
#     if i not in delete_index:
#         fixedTable.append(finalTable[i])


# print(len(fixedTable))

# fixedFinalTablePath = absPath + "/../mediated-schema/fixed-final-table.json"
# if os.path.exists(fixedFinalTablePath):
#     os.remove(fixedFinalTablePath)
# with open(fixedFinalTablePath, "w") as json_file:
#     json.dump(fixedTable, json_file, indent=4)





