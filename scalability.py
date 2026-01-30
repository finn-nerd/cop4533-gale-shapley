import time
import matplotlib.pyplot as plt

from verifier import verifier
from gale_shapley import gale_shapley
from data_helpers import generate_input


def main():
    """ (sara)
    Measures the running time of gale_shapley() and verifier() on progressively increasing n.
    Graphs the run time of each function using matplotlib line graph, with n on the x-axis and run time on the y-axis.
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