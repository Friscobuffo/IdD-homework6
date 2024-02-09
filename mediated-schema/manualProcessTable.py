import json
import os
import country_converter as coco
from multiprocessing import Process
import multiprocessing
from time import time
import shutil

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
FINAL_TABLE_PATH = ABS_PATH + "/final-table.json"
OUTPUT_DIRECTORY = ABS_PATH + "/processed-chunks"

def readJsonFile(filePath):
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

def saveJson(element, path):
    with open(path, "w") as jsonFile:
        json.dump(element, jsonFile, indent=4)

def removeNonNumerical(text):
    return ''.join(char for char in text if char.isdigit())

def removeAlpha(text):
    return ''.join(char for char in text if not char.isalpha())

def parseChunk(chunk, processNumber):
    # processing founding_year
    for entry in chunk:
        foundingYear = entry["founding_year"]
        foundingDate = entry["founding_date"]
        if (foundingYear == "" or foundingYear == "Not found"):
            if foundingDate != "":
                year = removeNonNumerical(foundingDate.split("/")[2])
                if len(year) == 4:
                    entry["founding_year"] = year
                    continue
            entry["founding_year"] = ""
            continue
        if len(foundingYear) == 4:
            continue
        onlyNumbers = removeAlpha(foundingYear)
        onlyNumbersList = onlyNumbers.split()
        actualFoundingYear = None
        for element in onlyNumbersList:
            element = removeNonNumerical(element)
            if len(element) == 4:
                actualFoundingYear = element
                break
        if actualFoundingYear:
            entry["founding_year"] =  actualFoundingYear
        else:
            entry["founding_year"] = ""

    # processing country
    i=0
    for entry in chunk:
        i+=1
        if i%15==0:
            print("process "+str(processNumber)+": "+str(round(i/len(chunk)*100, 2))+"%")
        country = entry["country"]
        components = country.split(",")
        if country.strip() == "":
            city = entry["location_city"]
            if not city: continue
            maybeCountry = entry["location_city"].split(",")[-1].strip()
            if not maybeCountry: continue
            processedCountry = coco.convert(maybeCountry, to='name')
            if processedCountry != "not found":
                entry["country"] = processedCountry
            continue
        if len(components)>1:
            last = components[-1].strip()
            processedCountry = coco.convert(last, to='name')
        else:
            processedCountry = coco.convert(components[0], to='name')
        if type(processedCountry) == list:
            processedCountry = processedCountry[-1] # maybe think better this thing
        if processedCountry == "not found":
            entry["country"] = ""
        else:
            entry["country"] = processedCountry
        if not entry["location_city"]:
            entry["location_city"] = country

    # saving json
    outputPath = OUTPUT_DIRECTORY + "/chunk" + str(processNumber) + ".json"
    saveJson(chunk, outputPath)
    print(f"finished {processNumber} process")

if __name__ == "__main__":
    if os.path.exists(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)
    os.mkdir(OUTPUT_DIRECTORY)
    finalTable = readJsonFile(FINAL_TABLE_PATH)
    start = time()
    numProcs = multiprocessing.cpu_count()
    procs = []
    totalEntries = len(finalTable)
    chunk_size = totalEntries // numProcs
    remainder = totalEntries - chunk_size*numProcs
    chunks = [finalTable[i : i + chunk_size] for i in range(0, totalEntries-remainder, chunk_size)]
    if remainder != 0:
        for i, elem in enumerate(finalTable[-remainder:]):
            chunks[i].append(elem)
    try:
        for i in range(numProcs):
            proc = Process(target=parseChunk, args=(chunks[i], i))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()
        totalTime = str(time() - start)
        print(f"total time: {totalTime}")
        files = os.listdir(OUTPUT_DIRECTORY)
        finalProcessedTable = []
        for file in files:
            finalProcessedTable += readJsonFile(OUTPUT_DIRECTORY + "/" + file)
        finalProcessedTablePath = ABS_PATH + "/processed-final-table.json"
        saveJson(finalProcessedTable, finalProcessedTablePath)
        # if os.path.exists(OUTPUT_DIRECTORY):
        #     shutil.rmtree(OUTPUT_DIRECTORY)
    except KeyboardInterrupt:
        print("\nclosing all processes")
        for proc in procs:
            proc.terminate()
        print("closed all processes")
        quit()