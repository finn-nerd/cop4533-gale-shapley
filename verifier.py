#!/usr/bin/env python3

from typing import List, Tuple, Dict
from data_helpers import parse_input, pack_input, parse_output, pack_output


def verifier(n: int, hospital_prefs: Dict[int, List[int]], student_prefs: Dict[int, List[int]], pairs: Dict[int, int]) -> bool:
    """ (sara)
    Takes in n, hospital_prefs, student_prefs matching gale_shapley() input, and pairs matching gale_shapley() output.
    Verifies that the each hospital and each student is matched exactly once.
    Verifies that all pairings are stable, with no blocking pairs.

    Prints either "VALID STABLE" if no blocking pairs and returns True,
    or "UNSTABLE [hospital, student]" for the first found blocking pair and returns False,
    or "INVALID (reason)" if the matching or input is invalid and returns False.
    """
    pass


def main():
    """ (sara)
    Measures the running time of gale_shapley() and verifier() on progressively increasing n.
    Graphs the run time of each function using matplotlib, with n on the x-axis and run time on the y-axis.
    Comment the trend of the graphs.
    """
    pass


if __name__ == "__main__":
    main()