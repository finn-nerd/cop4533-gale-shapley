#!/usr/bin/env python3

from typing import List, Tuple, Dict

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


def generate_input(n: int) -> Tuple[int, Dict[int, List[int]], Dict[int, List[int]]]:
    """ (sara)
    Takes in n, the number of hospitals / students.
    Generates and returns random hospital_prefs and student_prefs matching gale_shapley() input.
    hospital_prefs is a list of n lists, each containing a permutation of 1...n representing hospital i's preferences.
    student_prefs is the same format, but for students' preferences of hospitals.
    Returns n, hospital_prefs, student_prefs packed in a tuple.
    """
    pass


def generate_input_file(n: int) -> str:
    """ Shortcut function to generate input file for testing. """
    n, hospital_prefs, student_prefs = generate_input(n)
    return pack_input(n, hospital_prefs, student_prefs)


def parse_input(input_file: str) -> Tuple[int, Dict[int, List[int]], Dict[int, List[int]]]:
    """ (finn)
    Parse input from a file in the G-S input file format.
    Returns n, hospital_prefs, student_prefs (matching gale_shapley() input) packed in a tuple.
    """
    # Open file and fetch lines
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
    
    # Unpack line data
    n = int(lines[0])
    hospital_prefs = [list(map(int, lines[i].split())) for i in range(1, n + 1)]
    student_prefs = [list(map(int, lines[i].split())) for i in range(n + 1, 2 * n + 1)]
    
    return n, hospital_prefs, student_prefs


def pack_input(n: int, hospital_prefs: Dict[int, List[int]], student_prefs: Dict[int, List[int]]) -> str:
    """ (sara)
    Creates a .in file containing input in the G-S input file format.
    Creates a file "data/n.out" in the G-S input file format (where n is the number of hospitals / students).
    Returns the generated file name.
    """
    pass


def parse_output(output: str) -> Dict[int, int]:
    """ (sara)
    Parse output from a file in the G-S output file format.
    Returns output matching gale_shapley() output.
    """
    pass


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
    with open(filename, 'w') as f:
        for hospital in range(1, n + 1):
            student = output[hospital]
            f.write(f'{hospital} {student}\n')
    
    return filename