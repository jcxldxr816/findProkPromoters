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

def sanitizeString(file_path: str) -> str:
    """
    Reads a DNA sequence from a text file and removes
    whitespace and newline characters. Returns the cleaned string.
    """
    with open(file_path, "r") as f:        # Open the file in read mode
        data = f.read()                    # Read the entire file as a string
    if not data.strip():  # if file is empty or only spaces/newlines
        print("Error: The file is empty.")
        return ""
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
