# Finding Prokaryotic Promoters, part A
## findProkPromoters
CS325 Assignment 1a | Bioinformatics Group 3

# Program
This script takes a single DNA sequence string as input and verifies it is a valid sequence. It then finds exact matches to common promoter motifs/patterns and calculates an overall match score for each promoter.

## Program Flow
- User will input necessary information
- Input will be validated and sanitized
- Sequence will be checked for known promoters
- 

## Input
- DNA Sequence (likely as a standalone file)
- Scoring Parameters (input before(argparse) or during runtime)
- Known Promoter Patterns (OPTIONAL, probably unnecessary) (could be hardcoded or a separate file)

## Output
- Top three (?) scores and respective promoters found in sequence

# Data Organization
- We should use a dict/json to store known promoter sequences
- We need a way to keep track of located promoters, their locations, and their calculated match score **- James**
- We need to present output in a clean, easily readable manner. I think colors would be best **- James** (https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal)

# Functions
```python
sanitizeString(input: string) -> string  # Remove any whitespace, etc

validateDNAString(input: string) -> bool  # Takes DNA string, checks for any characters/nucleotides that do not belong

locatePromoters(promoterPattern: string) -> dict (or json?)  # Take string/dictionary value as input, output all matching strings and corresponding location/index in sequence
  #TODO may need to account for unknown/placeholder nucleotides, which would likely require a different function structure. could probably break into several functions

calculateMatchScore()
  #TODO not sure what this involves yet. We know the sequence that has been found is an exact match already, but we need to consider it's location and probably some other stuff... - James

outputBestMatches(quantity: int)  # Prints out specified number of best matches (descending order)
```
