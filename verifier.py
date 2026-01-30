#!/usr/bin/env python3
import os
from typing import List, Dict
from gale_shapley import gale_shapley
from data_helpers import read_input, read_pairs, parse_input, parse_output


def verifier(n: int, hospital_prefs: Dict[int, List[int]], student_prefs: Dict[int, List[int]], pairs: Dict[int, int]) -> bool:
    """ (sara)
    Takes in n, hospital_prefs, student_prefs matching gale_shapley() input, and pairs matching gale_shapley() output.
    Validity: Verifies that each hospital and each student is matched exactly once.
    Stability: Verifies that all pairings are stable, with no blocking pairs.

    Prints either "VALID STABLE" if no blocking pairs and returns True,
    or "UNSTABLE [hospital, student]" for the first found blocking pair and returns False,
    or "INVALID (reason)" if the matching or input is invalid and returns False.
    If both "UNSTABLE" and "INVALID", we'll output the first one to appear. 
    """

    # Since a dict maps one key to one value, each hospital and student are matched once unless the hospital/student is a duplicate or missing.

    # Check if there is a missing hospital in the final matchings.
    if(len(pairs) < n):
        print("INVALID (Missing Hospital)")
        return False
    
    # List to keep track of which students we've visited.
    visitedStudents = []

    # Create a dict that is reverse of pairs (matching with format (student, hospital)).
    reversePairs = {}

    # Dicts cannot have identical keys, meaning that there is automatically no duplicate hospitals.
    # We'll check for duplicate/missing students then.
    for hospital, student in pairs.items():
        # If this student was visited before, then this is a duplicate student and invalid. Else, we add student to visitedStudents.
        if(student in visitedStudents):
            print("INVALID (Duplicate Student in Final Matchings) ")
            return False
        else:
            visitedStudents.append(student)

        # We also check if the value of student == 0. If it is, this is our way to represent that a student is null/missing.
        if student == 0:
            print("INVALID (Missing Student for Hospital: " + str(hospital) + ")")
            return False

        # Add matching to reversePairs
        reversePairs[student] = hospital

    # We'll visit each possible pair of (hospital, student) and check if they are unstable.
    for hospital in range(1, n + 1):
        # Get the hospital's current assignment and preference list.
        currentStudent = pairs[hospital]
        hospitalList = hospital_prefs[hospital]

        for student in range(1, n + 1):
            # Bool to indicate if both hospital and student prefer each other.
            hospitalPrefer = False
            studentPrefer = False

            # Get indexes of the hospital's current assignment and new student.
            currentStudentIdx = hospitalList.index(currentStudent)
            newStudentIdx = hospitalList.index(student)

            # If the new student is more preferred than the hospital's current assignment, then indicate instability 1/2. 
            if newStudentIdx < currentStudentIdx:
                hospitalPrefer = True

            # Get student's current assignment and preference list.
            currentHospital = reversePairs[student]
            studentList = student_prefs[student]

            # Get indexes of the student's current assignment and new hospital.
            currentHospitalIdx = studentList.index(currentHospital)
            newHospitalIdx = studentList.index(hospital)

            # If the new hospital is more preferred than the student's current assignment, then indicate instability 2/2. 
            if newHospitalIdx < currentHospitalIdx:
                studentPrefer = True

            # If both the hospital and student prefer each other over their current assignment, they're unstable.
            if hospitalPrefer == True and studentPrefer == True:
                print("UNSTABLE [" + str(hospital) + ", " + str(student) + "]")
                return False

    # If made it here, matchings are valid and stable.
    print("VALID STABLE")
    return True

def main():
    # Choose input mode
    while True:
        mode = input("Which input method? file (1) or manual (2): ").strip()
        if mode in ("1", "2"):
            break
        print("Invalid choice. Enter 1 or 2.")

    if mode == "1":
        # .in file
        while True:
            in_path = input("Enter .in file path: ").strip()
            if in_path.endswith(".in") and os.path.isfile(in_path):
                n, hospital_prefs, student_prefs = parse_input(in_path)
                if n >= 1:
                    break
            print("Invalid .in file.")

        # Manual vs .out file
        while True:
            resp = input("Use existing .out pairings? (Y/N): ").strip().lower()
            if resp in ("y", "n"):
                break
            print("Enter Y or N.")
        if resp == "y":
            # .out file
            while True:
                out_path = input("Enter .out file path: ").strip()
                if out_path.endswith(".out") and os.path.isfile(out_path):
                    pairs = parse_output(out_path)
                    if len(pairs) >= 1:
                        break
                print("Invalid .out file.")
            
        else:
            # Use gale_shapley
            pairs = gale_shapley(n, hospital_prefs, student_prefs)
            print("----- Gale-Shapley Pairings -----")
            for hospital, student in pairs.items():
                print(f"{hospital} {student}")

    else:
        n, hospital_prefs, student_prefs = read_input()

        while True:
            resp = input("Manually output pairings? (Y/N): ").strip().lower()
            if resp in ("y", "n"):
                break
            print("Enter Y or N.")

        if resp == "y":
            pairs = read_pairs(n)
        else:
            pairs = gale_shapley(n, hospital_prefs, student_prefs)
            print("----- Gale-Shapley Pairings -----")
            for hospital, student in pairs.items():
                print(f"{hospital} {student}")
            

    print("Running verifier...")
    verifier(n, hospital_prefs, student_prefs, pairs)

if __name__ == "__main__":
    main()
