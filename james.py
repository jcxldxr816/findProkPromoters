import csv # standard library for reading and writing CSV files (Lib/csv.py)

# read from csv, send to this function
def calculateScore(queryString: str, motifString: str) -> float:
    queryLength: int = len(queryString)
    motifLength: int = len(motifString)
    
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
    print(f"Score: {score}")
    return score


# this function needs to return a score to the main function, 
# so it can be added to a new csv along with motif name and sequence

calculateScore('acacttccataatattttgatttcccacatatgtggataacttgggtagaa', 'acacttccataatattttgatttcccacatatgtggataacttgggtagaatggcgacccCttctcatcaggaagggttaa')