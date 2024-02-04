import os
import pickle

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
        print(key)
        print()
        print(score)
        print()
        matches[key] = score
# print(len(matches))