#!/usr/bin/env python3

from typing import List, Tuple, Dict
from data_helpers import parse_input, pack_input, parse_output, pack_output
import time
from gale_shapley import gale_shapley
from data_helpers import generate_input
import matplotlib.pyplot as plt


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
            print("INVALID (Missing Student for Hospital: " + hospital + ")")
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
                print("UNSTABLE [" + hospital + ", " + student + "]")
                return False

    # If made it here, matchings are valid and stable.
    print("VALID STABLE")
    return True



def main():
    """ (sara)
    Measures the running time of gale_shapley() and verifier() on progressively increasing n.
    Graphs the run time of each function using matplotlib line graph, with n on the x-axis and run time on the y-axis.
    Comment the trend of the graphs.
    """
    
    # Create a list of n to test.
    listN = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    # Create lists to record runtimes of gale_shapley() and verifier().
    listRunTimeGS = []
    listRunTimeV = []

    # Test each n and see how it affects runtime in gale_shapley() and verifier().
    for n in listN:
        # Get inputs for gale_shapley() and verifier().
        tempTuple = generate_input(n)
        hospitalPref = tempTuple[1]
        studentPref = tempTuple[2]

        dictGS = {}

        # Start and stop timer for running gale_shapley() with specific input.
        startGS = time.time()
        dictGS = gale_shapley(n, hospitalPref, studentPref)
        endGS = time.time()

        # Start and stop timer for running verifier() with specific input.
        startV = time.time()
        verifier(n, hospitalPref, studentPref, dictGS)
        endV = time.time()

        # Calculate running time and store in listRunTimeGS and listRunTimeV.
        runtimeGS = endGS - startGS
        runtimeV = endV - startV
        listRunTimeGS.append(runtimeGS)
        listRunTimeV.append(runtimeV)

    # Plot line graph of gale_shapley() runtimes.
    plt.subplot(1, 2, 1)
    plt.plot(listN, listRunTimeGS, color='blue', marker='o')
    plt.grid(True)
    plt.title("Runtimes of gale_shapley()")
    plt.xlabel("Input \"n\"")
    plt.ylabel("Runtime")

    # Plot line graph of verifier() runtimes.
    plt.subplot(1, 2, 2)
    plt.plot(listN, listRunTimeV, color='red', marker='o')
    plt.grid(True)
    plt.title("Runtimes of verifier()")
    plt.xlabel("Input \"n\"")
    plt.ylabel("Runtime")

    plt.suptitle("Runtimes for gale_shapley() and verifier()")
    plt.show()



if __name__ == "__main__":
    main()