"""
DNA Sequence Cleaner
--------------------

Purpose:
This program reads a DNA sequence from a text file,
removes unnecessary characters (spaces, line breaks),
and validates that the sequence only contains the
four standard DNA bases: A, T, C, G.

Biological context:
DNA sequences often come with formatting errors,
extra spaces, or invalid characters. For correct
biological analysis, only valid bases should be used.

Program flow:
1. Ask the user for the name of the input file.
2. Read the DNA sequence from the file and remove spaces/newlines.
3. Validate the sequence by keeping only A, T, C, G.
4. Print the intermediate and final results.

Usage:
$ python part1a_ashik.py
Enter the DNA file name: dna.txt

Output will show:
- The sequence after sanitization (step 2).
- The sequence after validation (step 3).
"""

import csv # Standard library for reading and writing CSV files (Lib/csv.py)
import datetime # Standard library for getting current time (Lib/datetime.py)
import heapq # Standard library for min-heap data structure. Used to track top X scores for quick output (Lib/heapq.py)

def sanitizeString(file_path: str) -> str:
    """
    Reads a DNA sequence from a text file and removes
    whitespace and newline characters. Returns the cleaned string.
    """
    with open(file_path, "r") as f:        # Open the file in read mode             #TODO we should validate input before working with file - James
        data = f.read()                    # Read the entire file as a string
    cleaned = data.replace(" ", "")        # Remove all spaces
    cleaned = cleaned.replace("\n", "")    # Remove all newlines
    return cleaned


def validateDNAString(dna_seq: str) -> str:
    """
    Takes a DNA sequence string and removes any characters
    that are not A, T, C, or G. Returns the cleaned DNA string.
    """
    valid_bases = "ATCG"   # Allowed characters
    cleaned = ""           # Start with empty string

    # Loop through each character in the input sequence
    for base in dna_seq.upper():   # Convert to uppercase (handles lowercase input)
        if base in valid_bases:    # Keep only A, T, C, G
            cleaned = cleaned + base   # Add valid base to output string

    return cleaned

# read from csv, send to this function
def calculateScore(query_string: str, motif_string: str) -> float:
    query_length: int = len(query_string)
    motif_length: int = len(motif_string)

    motif_string = motif_string.upper()
    
    # Adding junk characters to end to make strings equal length
    diff: int = query_length - motif_length
    if diff < 0: # Motif is longer than Query
        for i in range(0, abs(diff)):
            query_string += 'X'
    elif diff > 0: # Query is longer than Motif
        for i in range(0, diff):
            motif_string += 'X'

    # Comparing the characters between the two strings
    matching_character_count: int = 0
    for index, char in enumerate(motif_string): # Using index to ensure character positions align for comparison
        if (motif_string[index] == query_string[index]):
            matching_character_count += 1 # Keeping track of correct/matching characters

    score: float = (matching_character_count / len(motif_string)) * 100.0 # Calculating a percentage of correct/matching characters
    return score

def readFromCSV(file_to_read: str) -> list:
    with open(file_to_read, 'r', newline='') as motif_file: #TODO we should validate input before working with file - James
        reader = csv.DictReader(motif_file)
        data_from_file = list(reader) # is a list of dictionaries (each row is a dict)
    return data_from_file

def writeToCSV(data_to_write: list, output_destination: str):
    fieldnames = data_to_write[0].keys() # Updating column names to include the newly added 'Score' column
    with open(output_destination, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_to_write)
        print(f"Successfully created output file: {output_destination}")

def outputQuickOverview(data_to_sort: list, amount_to_display: int):
    top_scores = []
    for index, row in enumerate(data_to_sort):
        score = row["Score"]
        motif_entry = (score, index, row) # Using index as a tiebreaker value for heap comparison. heapq can't compare equal values

        if len(top_scores) < amount_to_display:
            heapq.heappush(top_scores, motif_entry)
        else:
            heapq.heappushpop(top_scores, motif_entry) # This pops(removes) the smallest value from the heap
    top_scores = sorted(top_scores, key=lambda x: x[0], reverse=True) # Sorting by scores
    for score, _, row in top_scores:
        print(f"Promoter ID: {row['id']}\t||\tScore: {score}")

if __name__ == "__main__":
    # Step 1: Ask the user to type the file name
    file_name = input("Enter the DNA file name: ")

    # Step 2: Sanitize (remove spaces/newlines)
    cleaned_string = sanitizeString(file_name)

    # Step 3: Validate (remove invalid characters)
    validated_string = validateDNAString(cleaned_string)

    # Step 4: Print results for the user
    # print("After sanitize:", cleaned)
    # print("After validate:", validated)
    print("Here is the cleaned input DNA sequence:", validated_string)

    # Step 5: Ask user to specify a .csv file to use as motifs
    motif_csv_file = input("Enter the motif file name (.csv): ")
    print("Comparing DNA sequence to known promoters. This may take a while...")

    # Step 6: Read from csv file
    motif_data = readFromCSV(motif_csv_file)

    # Step 7: Calculate score for every row in csv
    for row in motif_data:
        row['Score'] = calculateScore(validated_string, row['PromoterSeq']) # Adding score to motif_data

    # Step 8: Write results to new csv file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # getting timestamp to keep file names unique
    output_filename = f"./output/output_{timestamp}.csv" # Name used for file output
    writeToCSV(motif_data, output_filename)

    # Step 9: Display quick overview of results in terminal
    print("Printing scores!")
    outputQuickOverview(motif_data, 3) # Printing top 3 scores in terminal.