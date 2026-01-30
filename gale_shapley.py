#!/usr/bin/env python3

from typing import List, Dict
from data_helpers import valid_input, read_input


def gale_shapley(n: int, hospital_preferences: Dict[int, List[int]], student_preferences: Dict[int, List[int]]) -> Dict[int, int]:
    """ (finn)
    Input:
        n: number of hospitals / students
        hospital_prefs: dict of hospital preferences, associating [hospital, [student preference list]]
        hospital_prefs: dict of hospital preferences, associating [hospital, [student preference list]]
        student_prefs: same format as hospital_prefs, but for students' preferences of hospitals
    Output:
        A dict of formed pairs using hospitals as keys and students as values [hospital, student]
    """

    ###### Initialization ######

    if not valid_input(n, hospital_preferences, student_preferences):
        return {}

    # Copy input lists to avoid modifying them
    hospital_prefs = {i: hospital_preferences[i][:] for i in hospital_preferences}
    student_prefs = {i: student_preferences[i][:] for i in student_preferences}
    
    # Initialize a list with all free hospitals
    free_hospitals = list(range(1, n + 1))
    
    # Initialize a list to keep track of paired students (0 = unpaired, x = hospital paired to)
    paired_students = [0] * (n + 1) # index 0 unused, no "0" student


    ###### Gale-Shapley ######
        
    pairings = {}
    while free_hospitals:
        
        # Pick an unmatched hospital, iterate over its preference list
        hospital = free_hospitals.pop(0)
        
        # While the hospital has untested pairs
        while hospital_prefs[hospital]:

            # Fetch most preferred student
            student = hospital_prefs[hospital].pop(0)

            # If student is free, pair it with hospital
            if paired_students[student] == 0:
                pairings[hospital] = student
                paired_students[student] = hospital
                break

            # If student is paired but prefers this hospital, break old pair and create new one
            # This comparison makes it n^3, but I don't feel like adding a quick-lookup ranking map
            old_hospital = paired_students[student]
            if student_prefs[student].index(hospital) < student_prefs[student].index(old_hospital):
                pairings.pop(old_hospital) # break prev. pair
                free_hospitals.insert(0, old_hospital) # re-add to free hospitals
                pairings[hospital] = student # create new pair
                paired_students[student] = hospital
                break

            # Student rejects pairing with this hospital
            continue

    return pairings


def main():
    """ (finn)
    Runnable from command line:
        cat input.in | python gale-shapley.py
        OR
        python gale-shapley.py
            which will prompt for input using stdin in the format:
            n
            hospital_prefs  ] n lines, n numbers long each
            student_prefs   ] n lines, n numbers long each
    """
    n, hospital_prefs, student_prefs = read_input()

    # Run algorithm and print results
    print("----- Gale-Shapley Pairings -----")
    result = gale_shapley(n, hospital_prefs, student_prefs)
    for hospital, student in result.items():
        print(f"{hospital} {student}")


if __name__ == "__main__":
    main()
