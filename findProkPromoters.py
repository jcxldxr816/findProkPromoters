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
def calculateScore(queryString: str, motifString: str) -> float:
    queryLength: int = len(queryString)
    motifLength: int = len(motifString)

    motifString = motifString.upper()
    
    # Adding junk characters to end to make strings equal length
    diff: int = queryLength - motifLength
    if diff < 0: # Motif is longer than Query
        for i in range(0, abs(diff)):
            queryString += 'X'
    elif diff > 0: # Query is longer than Motif
        for i in range(0, diff):
            motifString += 'X'
    # Sequences should now be equal lengths.

    # Comparing the characters between the two strings
    matchingCharCount: int = 0
    for index, char in enumerate(motifString): # Using index to ensure character positions align for comparison
        if (motifString[index] == queryString[index]):
            matchingCharCount += 1 # Keeping track of correct/matching characters

    score: float = (matchingCharCount / len(motifString)) * 100.0 # Calculating a percentage of correct/matching characters
    return score

if __name__ == "__main__":
    # Step 1: Ask the user to type the file name
    file_name = input("Enter the DNA file name: ")

    # Step 2: Sanitize (remove spaces/newlines)
    cleaned = sanitizeString(file_name)

    # Step 3: Validate (remove invalid characters)
    validated = validateDNAString(cleaned)

    # Step 4: Print results for the user
    print("After sanitize:", cleaned)
    print("After validate:", validated)

    # Step 5: Ask user to specify a .csv file to use as motifs
    motif_csv_file = input("Enter the motif file name (.csv): ")

    # Step 6: Read from csv file
    column_values = []
    with open(motif_csv_file, 'r', newline='') as motif_file: #TODO we should validate input before working with file - James
        reader = csv.DictReader(motif_file)
        motif_data = list(reader)

    # Step 7: Calculate score for every row in csv
    for row in motif_data:
        row['Score'] = calculateScore(validated, row['PromoterSeq']) # Adding score to motif_data

    # Step 8: Write results to new csv file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"output_{timestamp}.csv" # Name used for file output
    
    fieldnames = motif_data[0].keys() # Updating column names to include the newly added 'Score' column
    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(motif_data)
        print(f"Successfully created output file: {output_filename}")