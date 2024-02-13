import os
import pandas as pd
import matplotlib.pyplot as plt

def file_histogram(directory):
    # Get the list of files in the directory
    files = os.listdir(directory)
    # Create dictionaries to store file names and entry counts
    sum_files = 0
    tot_comparisons = 0
    # Iterate over each file
    for file in files:
        # Read the JSON file into a DataFrame
        try:
            data = pd.read_json(os.path.join(directory, file))
        except ValueError:
            print(f"Error reading file: {file}. Skipping...")
            continue

        tot_comparisons += (len(data) * (len(data) - 1))/2

        sum_files+=1
    
        
    print(tot_comparisons/sum_files) # numero medio di confronti
        


# Call the function with the directory path
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
TABLE_PATH = os.path.join(ABS_PATH + '/pairwise-matching/output')
file_histogram(TABLE_PATH)