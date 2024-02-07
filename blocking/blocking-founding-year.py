import json
import os

def readJsonFile(filePath):
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

def removeNonNumerical(text):
    return ''.join(char for char in text if char.isdigit())

def removeAlpha(text):
    return ''.join(char for char in text if not char.isalpha())

def addResult(results, entry, year):
    if year in results:
        l = results[year]
        l.append(entry)
        return
    l = [entry]
    results[year] = l

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABS_PATH)
FINAL_TABLE_PATH = PARENT_DIR + "/mediated-schema/final-table.json"

finalTable = readJsonFile(FINAL_TABLE_PATH)
results = dict()
for entry in finalTable:
    foundingYear = entry["founding_year"]
    foundingDate = entry["founding_date"]
    if (foundingYear == "" or foundingYear == "Not found"):
        if foundingDate != "":
            year = removeNonNumerical(foundingDate.split("/")[2])
            if len(year) == 4:
                addResult(results, entry, year)
                continue
        addResult(results, entry, "")
        continue
    if len(foundingYear) == 4:
        addResult(results, entry, foundingYear)
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
        addResult(results, entry, actualFoundingYear)
    else:
        addResult(results, entry, "")

blockingFoundingYearPath = ABS_PATH + "/blocking-founding-year.json"
if os.path.exists(blockingFoundingYearPath):
    os.remove(blockingFoundingYearPath)
with open(blockingFoundingYearPath, "w") as json_file:
    json.dump(results, json_file, indent=4)