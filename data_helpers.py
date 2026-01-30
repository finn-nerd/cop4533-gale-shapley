#!/usr/bin/env python3

from typing import List, Tuple, Dict
import random

"""
G-S input file format:
    n               ] integer number of hospitals / students
    hospital_prefs  ] n lines, each a permutation of 1...n representing hospital preferences
    student_prefs   ] n lines, each a permutation of 1...n representing student preferences
Example:
    3
    1 2 3
    2 3 1
    2 1 3
    2 1 3
    1 2 3
    1 2 3

G-S output file format:
    [hospital 1, paired student] pairing
    [hospital 2, paired student] pairing
    ...
    [hospital n, paired student] pairing
Example:
    1 2
    2 3
    3 1
"""


def valid_input(n: int, hospital_prefs: Dict[int, List[int]], student_prefs: Dict[int, List[int]]) -> bool:
    if n < 1:
        print("Input Error: n must be at least 1.")
        return False

    if len(hospital_prefs) != n or len(student_prefs) != n:
        print("Input Error: Hospital/student count not equal to n.")
        return False

    # Keys must be exactly 1..n
    valid_keys = set(range(1, n + 1))
    if set(hospital_prefs.keys()) != valid_keys:
        print("Input Error: Hospital keys must be exactly 1..n.")
        return False
    if set(student_prefs.keys()) != valid_keys:
        print("Input Error: Student keys must be exactly 1..n.")
        return False

    # Preference values must be exactly 1..n
    for hospital, prefs in hospital_prefs.items():
        if len(set(prefs)) != n:
            print(f"Input Error: Hospital {hospital}'s preference list contains duplicates or invalid entries.")
            return False
        if set(prefs) != valid_keys:
            print(f"Input Error: Hospital {hospital}'s preference list is not a permutation of 1..n.")
            return False

    for student, prefs in student_prefs.items():
        if len(set(prefs)) != n:
            print(f"Input Error: Student {student}'s preference list contains duplicates or invalid entries.")
            return False
        if set(prefs) != valid_keys:
            print(f"Input Error: Student {student}'s preference list is not a permutation of 1..n.")
            return False
        
    return True


def generate_input(n: int) -> Tuple[int, Dict[int, List[int]], Dict[int, List[int]]]:
    """ (sara)
    Takes in n, the number of hospitals / students.
    Generates and returns random hospital_prefs and student_prefs matching gale_shapley() input.
    hospital_prefs is a list of n lists, each containing a permutation of 1...n representing hospital i's preferences.
    student_prefs is the same format, but for students' preferences of hospitals.
    Returns n, hospital_prefs, student_prefs packed in a tuple.
    """

    # Populate a list of n hospitals/students.
    ogList = []
    for num in range(1, n + 1):
        ogList.append(num)

    hospitalDict = {}
    studentDict = {}

    # Loop through each hospital/student and add them and their preference list to their respective dict.
    for num in range(1, n + 1):
        # Shuffle ogList to get randomized preference lists for hospitals/students.
        random.shuffle(ogList)
        hospitalDict[num] = ogList.copy()

        random.shuffle(ogList)
        studentDict[num] = ogList.copy()

    resultTuple = (n, hospitalDict, studentDict)

    return resultTuple

def generate_input_file(n: int) -> str:
    """ Shortcut function to generate input file for testing. """
    n, hospital_prefs, student_prefs = generate_input(n)
    return pack_input(n, hospital_prefs, student_prefs)


def parse_input(input_file: str) -> Tuple[int, Dict[int, List[int]], Dict[int, List[int]]]:
    """ (finn)
    Parse input from a file in the G-S input file format.
    Returns n, hospital_prefs, student_prefs (matching gale_shapley() input) packed in a tuple.
    """
    # Attempt to Open File
    try:
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Parse_Input Error: input file not found")
        return -1, None, None
    except OSError as e:
        print(f"Parse_Input Error opening file: {e}")
        return -1, None, None

    if not lines:
        print("Parse_Input Error: input file is empty")
        return -1, None, None

    # Parse n
    try:
        n = int(lines[0])
    except ValueError:
        print("Parse_Input Error: first line must be an integer (n)")
        return -1, None, None
    if n <= 0:
        print("Parse_Input Error: n must be positive")
        return -1, None, None


    # Check line amount
    expected_lines = 1 + 2 * n
    if len(lines) != expected_lines:
        print(f"Parse_Input Error: expected {expected_lines} lines, got {len(lines)}")
        return -1, None, None

    # Parse preferences
    try:
        hospital_lists = [list(map(int, lines[i].split())) for i in range(1, n + 1)]
        student_lists  = [list(map(int, lines[i].split())) for i in range(n + 1, 2 * n + 1)]
    except ValueError:
        print("Parse_Input Error: preferences must contain integers only")
        return -1, None, None
    
    # Convert preference lists to dicts
    hospital_prefs = {i + 1: hospital_lists[i] for i in range(n)}
    student_prefs  = {i + 1: student_lists[i]  for i in range(n)}

    # Validate preference lists
    if not valid_input(n, hospital_prefs, student_prefs):
        return -1, None, None

    # Return successfully
    return n, hospital_prefs, student_prefs


def pack_input(n: int, hospital_prefs: Dict[int, List[int]], student_prefs: Dict[int, List[int]]) -> str:
    """ (sara)
    Creates a .in file containing input in the G-S input file format.
    Creates a file "data/n.out" in the G-S input file format (where n is the number of hospitals / students).
    Returns the generated file name.
    """

    if not valid_input(n, hospital_prefs, student_prefs):
        return ""

    # Create .in file.
    filename = f"data/{n}.in"

    # Write hospital_prefs and student_prefs to file.
    with open(filename, "w") as f:
        f.write(f"{n}\n")

        # Write each hospital's preference list to file.
        for hospital in range(1, n + 1):
            # Get's hospital's preference list.
            prefs = hospital_prefs[hospital]

            # Converts ints to strings and joins them with spaces.
            f.write(" ".join(map(str, prefs)) + "\n")

        # Write each student's preference list to file.
        for student in range(1, n + 1):
            # Get's hospital's preference list.
            prefs = student_prefs[student]

            # Converts numbers to strings and joins them with spaces.
            f.write(" ".join(map(str, prefs)) + "\n")

    return filename


def parse_output(filename: str) -> Dict[int, int]:
    """ (sara)
    Parse output from a file in the G-S output file format.
    Returns output matching gale_shapley() output.
    """

    pairs = {}

    # Read in file contents.
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            # If its an empty line, continue.
            if not line:
                continue

            # Check if the line doesn't have 2 items in it.
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Invalid output line: '{line}'")

            # Put hospital, student into pairs.
            hospital, student = map(int, parts)
            pairs[hospital] = student

    return pairs


def pack_output(output: Dict[int, int]) -> str:
    """ (finn)
    Takes in input matching gale_shapley() output.
    Creates a file "data/n.out" in the G-S output file format (where n is the number of hospitals / students).
    Returns the generated file name.
    """
    # Create .out file
    n = len(output)
    filename = f'data/{n}.out'
    
    # Write pairs to file
    try:
        with open(filename, 'w') as f:
            for hospital in range(1, n + 1):
                student = output[hospital]  # may KeyError
                f.write(f"{hospital} {student}\n")
    except KeyError as e:
        print(f"Pack_Output Error: missing hospital key {e}")
        return ""
    
    return filename