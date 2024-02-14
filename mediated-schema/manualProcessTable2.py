import os
import json
from geopy.geocoders import Nominatim
from geopy.geocoders import Bing
import country_converter as coco
import translators as ts
import re
import sys
from time import time

start = time()

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FINAL_TABLE_PATH = ABS_PATH + "/processed-final-table.json"

with open(PROCESSED_FINAL_TABLE_PATH, 'r') as jsonfile:
    processedFinalTable = json.load(jsonfile)

total = 0
for entry in processedFinalTable:
    country = entry["country"]
    city = entry["location_city"]
    if not country and city:
        total += 1
# geolocator = Nominatim(user_agent="gino")
geolocator = Bing(user_agent="piripicchio", api_key="")
i = 0

countryLabels = dict()
def processCountryCoco(country, labels):
    if country in labels:
        return labels[country]
    processedCountry = coco.convert(country, to='name')
    if processedCountry != "not found":
        labels[country] = processedCountry
        return processedCountry
    label = ts.translate_text(country, translator="google")
    label = coco.convert(label, to="name")
    labels[country] = label
    return label

def geolocate(city, errors=0):
    try:
        location = geolocator.geocode(city)
    except Exception:
        if errors == 3:
            print("too many errors, saving cache before exiting")
            with open(CACHE_PATH, "w") as jsonFile:
                json.dump(cache, jsonFile, indent=4)
            sys.exit()
        location = geolocate(city, errors+1)
    return location

CACHE_PATH = ABS_PATH + "/cache.json"
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, 'r') as jsonfile:
        cache = json.load(jsonfile)
else:
    cache = dict()
cacheHits = 0
errors = 0
print(total)
allCountriesOccurrences = dict()
for entry in processedFinalTable:
    country = entry["country"]
    city = entry["location_city"]
    if (not country) and city:
        i += 1
        print(f"i: {str(i)} cache size: {len(cache)} cache hits: {cacheHits} errors: {errors}")
        if re.match(r'^IT\d{11}$', city):
            country = processCountryCoco("Italy", countryLabels)
            entry["country"] = country
            continue
        if city in cache:
            cacheHits += 1
            country = cache[city]
            if country != "not found":
                entry["country"] = country
                if country not in allCountriesOccurrences:
                    allCountriesOccurrences[country] = 0
                allCountriesOccurrences[country] += 1
            continue
        location = geolocate(city)
        if location == None:
            last = city.split(",")[-1]
            location = geolocate(last)
            if location == None:
                print("\nlocation still None :(")
                print(city)
                continue
        country = location.address.split(",")[-1].strip()
        processedCountry = processCountryCoco(country, countryLabels)
        if processedCountry and (processedCountry != "not found"):
            entry["country"] = processedCountry
            if processedCountry not in allCountriesOccurrences:
                allCountriesOccurrences[processedCountry] = 0
            allCountriesOccurrences[processedCountry] += 1
        else:
            print(f"not found this {city}")
            errors += 1
        cache[city] = processedCountry

PROCESSED_FINAL_TABLE_PATH2 = ABS_PATH + "/processed-final-table2.json"
with open(PROCESSED_FINAL_TABLE_PATH2, "w") as jsonFile:
    json.dump(processedFinalTable, jsonFile, indent=4)

for country in allCountriesOccurrences:
    print(f"{country} occurrences: {allCountriesOccurrences[country]}")

print(f"total time: {time()- start}")