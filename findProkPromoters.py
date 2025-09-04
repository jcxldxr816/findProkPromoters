"""
DNA Sequence Promoter Finder
----------------------------

Purpose:
This program reads a DNA sequence from a text file,
removes unnecessary characters (spaces, line breaks),
and validates that the sequence only contains the
four standard DNA bases: A, T, C, G.

It then compares the cleaned DNA sequence to known
promoter motifs stored in a CSV file, calculates
similarity scores, writes the results to a new CSV
file, and prints a quick summary of the best matches.

Biological context:
Promoters are short DNA motifs that signal where
gene transcription should begin. Identifying these
motifs helps us predict gene expression patterns.

Program flow:
1. Ask the user for the DNA file name.
2. Sanitize the DNA (remove spaces/newlines).
3. Validate the DNA (keep only A, T, C, G).
4. Print the cleaned DNA sequence.
5. Ask the user for a promoter motifs CSV file.
6. Read promoter motifs from the CSV file.
7. Compare DNA sequence to motifs and calculate scores.
8. Save results to a timestamped CSV file.
9. Print the highest scoring motifs in the terminal.

Usage:
$ python findProkPromoter.py
"""


import csv # Standard library for reading and writing CSV files (Lib/csv.py)
import datetime # Standard library for getting current time (Lib/datetime.py)
import heapq # Standard library for min-heap data structure. Used to track top X scores for quick output (Lib/heapq.py)
import sys  # Standard library for exiting program on invalid input

def sanitizeString(file_path: str) -> str:
    """
    Reads a DNA sequence from a text file and removes
    whitespace and newline characters. Returns the cleaned string.
    """
    if file_path.endswith('.txt') == False:
        print("Error: Please enter a valid .txt filename")
        sys.exit()
    with open(file_path, "r") as f:        # Open the file in read mode
        data = f.read()                    # Read the entire file as a string
    if not data.strip():  # if file is empty or only spaces/newlines
        print("Error: The file is empty.")
        sys.exit()
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
def calculateScore(query_string: str, motif_string: str): # returns float, list
    """
    Calculates the percentage of identical characters between the query string and the motif string.
    Returns a score, and list of character-mismatch locations/indices
    """
    query_length: int = len(query_string)
    motif_length: int = len(motif_string)

    motif_string = motif_string.upper()
    
    # Adding junk characters to end to make strings equal length
    diff: int = query_length - motif_length
    if diff < 0:                        # Motif is longer than Query
        for i in range(0, abs(diff)):
            query_string += 'X'
    elif diff > 0:                      # Query is longer than Motif
        for i in range(0, diff):
            motif_string += 'X'

    # Comparing the characters between the two strings
    matching_character_count: int = 0
    mismatch_indexes: list = [motif_string]     # This will be used to indicate where sequences do not match
    for index, char in enumerate(motif_string): # Using index to ensure character positions align for comparison
        if (motif_string[index] == query_string[index]):
            matching_character_count += 1       # Keeping track of correct/matching characters
        else:
            mismatch_indexes.append(index)

    score: float = (matching_character_count / len(motif_string)) * 100.0 # Calculating a percentage of correct/matching characters
    return score, mismatch_indexes

def readFromCSV(file_to_read: str) -> list:
    """
    Reads from source CSV file, which should contain known promoter motifs.
    """
    if file_to_read.endswith('.csv') == False:
        print("Error: Please enter a valid .csv filename")
        sys.exit()
    print("Comparing DNA sequence to known promoters. This may take a while...\n")
    with open(file_to_read, 'r', newline='') as motif_file: #TODO we should validate input before working with file - James
        reader = csv.DictReader(motif_file)
        data_from_file = list(reader) # is a list of dictionaries (each row is a dict)
    return data_from_file

def writeToCSV(data_to_write: list, output_destination: str):
    """
    Writes to an output CSV file, updating columns, since we add a column to store the match score.
    Takes as input the data to be written, and the destination/filename
    """
    fieldnames = data_to_write[0].keys() # Updating column names to include the newly added 'Score' column
    with open(output_destination, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_to_write)
        print(f"Successfully created output file: {output_destination}")

def outputQuickOverview(data_to_sort: list, amount_to_display: int, mismatch_masterlist: list):
    """
    Provides a quick overview of script results in the terminal.
    Takes as input the promoter motif CSV data, after score calculation.
    Takes as input the desired number of results to display.
    Takes as input the list of lists detailing character mismatch locations.
    """
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
        error_indicator_string: str = '_' * len(row['PromoterSeq']) # Populating error indicator line with blanks


        for error_indices_list in mismatch_masterlist:
            if error_indices_list[0] == row['PromoterSeq'].upper(): # Checking for error data on top score strings
                for i in range(1, len(error_indices_list)):
                    # Replacing blank with a red X to indicate mismatch
                    error_indicator_string = error_indicator_string[:error_indices_list[i]] + "X" + error_indicator_string[error_indices_list[i]+1:]

        print(f"Promoter ID: {row['id']}\t\tScore: {score:.3f}")
        print(f"DNA Sequence: \t\t{validated_string}")
        print(f"Promoter Sequence: \t{row['PromoterSeq'].upper()}")
        print(f"Mismatch View: \t\t\033[31m{error_indicator_string}\033[0m\n")

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
    print("Here is the cleaned input DNA sequence:", validated_string, "\n")

    # Step 5: Ask user to specify a .csv file to use as motifs
    motif_csv_file = input("Enter the motif file name (.csv): ")

    # Step 6: Read from csv file
    motif_data = readFromCSV(motif_csv_file)

    # Step 7: Calculate score for every row in csv
    mismatch_list_list = [] # this will store lists for any row above the threshold specified below
    for row in motif_data:
        row['Score'], mismatches = calculateScore(validated_string, row['PromoterSeq']) # Adding score to motif_data
        if row['Score'] > 25.0:
            mismatch_list_list.append(mismatches)

    # Step 8: Write results to new csv file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # getting timestamp to keep file names unique
    output_filename = f"./output/output_{timestamp}.csv" # Name used for file output
    writeToCSV(motif_data, output_filename)

    # Step 9: Display quick overview of results in terminal
    print("Printing scores!\n")
    outputQuickOverview(motif_data, 3, mismatch_list_list) # Printing top 3 scores in terminal.