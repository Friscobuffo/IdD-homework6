import os
import pickle
import shutil

absPath = os.path.dirname(os.path.abspath(__file__))
MATCHES_DIRECTORY = absPath + "/matches"
allMatches = os.listdir(MATCHES_DIRECTORY)
matches = dict()
for fileName in allMatches:
    filePath = MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'rb') as pickleFile:
        m = pickle.load(pickleFile)
    for key in m:
        score = m[key]
        if score>0.3: matches[key] = score
sets = []
for key in matches:
    dataset0 = key[0]
    dataset1 = key[1]
    combined = set()
    combined.add(dataset0)
    combined.add(dataset1)
    j = 0
    for s in sets:
        if dataset0 in s:
            temp = sets.pop(j)
            combined = combined.union(temp)
        j += 1
    j = 0
    for s in sets:
        if dataset0 in s:
            temp = sets.pop(j)
            combined = combined.union(temp)
        j += 1
    sets.append(combined)

absPath = os.path.dirname(os.path.abspath(__file__))
PROCESSED_MATCHES_DIRECTORY = absPath + "/processed-matches"
if os.path.exists(PROCESSED_MATCHES_DIRECTORY):
    shutil.rmtree(PROCESSED_MATCHES_DIRECTORY)
os.mkdir(PROCESSED_MATCHES_DIRECTORY)
for i, s in enumerate(sets):
    fileName = "matches"+str(i)+".txt"
    filePath = PROCESSED_MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'w') as f:
        for elem in s:
            f.write(str(elem) + '\n')