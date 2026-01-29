#!/usr/bin/env python3

from typing import List, Dict


def gale_shapley(n: int, hospital_prefs: Dict[int, List[int]], student_prefs: Dict[int, List[int]]) -> Dict[int, int]:
    """ (finn)
    Input:
        n: number of hospitals / students
        hospital_prefs: dict of hospital preferences, associating [hospital, [student preference list]]
        student_prefs: same format as hospital_prefs, but for students' preferences of hospitals
    Output:
        A dict of formed pairs using hospitals as keys and students as values [hospital, student]
    """

    pass


def main():
    """ (finn)
    Runnable from command line:
        python gale-shapley.py < input.in
        OR
        python gale-shapley.py
            which will prompt for input using stdin in the format:
            n
            hospital_prefs  ] n lines, n numbers long each
            student_prefs   ] n lines, n numbers long each
    """
    return


if __name__ == "__main__":
    main()
