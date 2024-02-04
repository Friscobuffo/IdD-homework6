import os
import pickle
from multiprocessing import Process
from time import time
from valentine import valentine_match
from valentine.algorithms import Coma
import pandas as pd
import shutil

absPath = os.path.dirname(os.path.abspath(__file__))
MATCHES_DIRECTORY = absPath + "/matches"

def parseChunk(chunk, schemaList, schemaNames, processNumber):
    matcher = Coma(use_instances=True, java_xmx="2048m")
    matches = dict()
    n = 0
    for comparison in chunk:
        n += 1
        print(n)
        i = comparison[0]
        j = comparison[1]
        result = valentine_match(schemaList[i], schemaList[j], matcher, schemaNames[i], schemaNames[j])
        for key in result:
            score = result[key]
            matches[key] = score
    print(f"finished {processNumber} process")
    pickle.dump(matches, open(MATCHES_DIRECTORY+"/matches"+str(processNumber), 'wb'))

if __name__ == "__main__":
    start = time()
    # numProcs = multiprocessing.cpu_count()
    numProcs = 2
    procs = []
    parsers = []
    dataSource = absPath + "/sources-json"
    files = os.listdir(dataSource)
    schemaList = []
    schemaNames = []
    for file in files:
        filePath = dataSource + "/" + file
        df = pd.read_json(filePath)
        df = df.iloc[:500]
        schemaList.append(df)
        schemaNames.append(file)
    totalSchemas = len(schemaList)
    totalComparisons = totalSchemas*(totalSchemas-1)//2
    comparisons = []
    chunk_size = totalComparisons // numProcs
    remainder = totalComparisons - chunk_size*numProcs
    for i in range(totalSchemas-1):
        for j in range(i+1, totalSchemas):
            comparisons.append((i,j))
    chunks = [comparisons[i : i + chunk_size] for i in range(0, len(comparisons)-remainder, chunk_size)]
    if remainder != 0:
        for i, elem in enumerate(comparisons[-remainder:]):
            chunks[i].append(elem)
    if os.path.exists(MATCHES_DIRECTORY):
        shutil.rmtree(MATCHES_DIRECTORY)
    os.mkdir(MATCHES_DIRECTORY)
    try:
        for i in range(numProcs):
            proc = Process(target=parseChunk, args=(chunks[i], schemaList, schemaNames, i))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()
        totalTime = str(time() - start)
        print(f"total time: {totalTime}")
    except KeyboardInterrupt:
        print("\nclosing all processes")
        for proc in procs:
            proc.terminate()
        print("closed all processes")