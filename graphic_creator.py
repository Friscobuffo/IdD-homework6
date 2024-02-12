import os
import pandas as pd
import matplotlib.pyplot as plt

def file_histogram(directory):
    # Get the list of files in the directory
    files = os.listdir(directory)
    # Create dictionaries to store file names and entry counts
    file_entries = {}

    # Iterate over each file
    for file in files:
        # Read the JSON file into a DataFrame
        try:
            data = pd.read_json(os.path.join(directory, file))
        except ValueError:
            print(f"Error reading file: {file}. Skipping...")
            continue

        # Count the number of entries for the current file
        num_entries = len(data)
        
        file_name = os.path.splitext(file)[0]
        # Store the file name and entry count
        file_entries[file_name] = num_entries

    # Sort files based on the number of entries
    sorted_files = sorted(file_entries.items(), key=lambda x: x[1], reverse=True)

    # Create lists to store file names and entry counts
    file_names = []
    entry_counts = []

    # Iterate over sorted files
    for file, num_entries in sorted_files:
        file_names.append(file)
        entry_counts.append(num_entries)

    # Plot the histogram
    plt.figure(facecolor='#37474f')  # Set figure background color
    plt.bar(file_names, entry_counts, color='darkcyan')  # Bar color
    plt.xlabel('File Names', color='white')  # X-axis label color
    plt.ylabel('Number of Entries', color='white')  # Y-axis label color
    plt.title('Entries for country', color='white')  # Title color
    plt.xticks(color='white')  # X-axis tick labels color
    plt.yticks(color='white')  # Y-axis tick labels color
    plt.grid(axis='y', linestyle='--', color='gray')  # Grid color

    # Calculate average number of entries
    average_entries = sum(entry_counts) // len(entry_counts)

    # Plot average line
    plt.axhline(y=average_entries, color='red', linestyle='--', linewidth=0.9, label=f'Average: ~{average_entries:.2f}')
    plt.legend()

    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent overlap of labels
    plt.show()

# Call the function with the directory path
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
TABLE_PATH = os.path.join(ABS_PATH + '/sources-json')
file_histogram(TABLE_PATH)