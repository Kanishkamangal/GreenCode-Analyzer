# Benchmark: Bubble Sort
# Category: Sorting
# Algorithm: Bubble Sort - O(n^2)

import sys


def main():

    data = list(map(int, sys.stdin.buffer.read().split()))

    n = len(data)

    for i in range(n - 1):

        swapped = False

        for j in range(n - i - 1):

            if data[j] > data[j + 1]:

                data[j], data[j + 1] = data[j + 1], data[j]

                swapped = True

        if not swapped:
            break

    print(data[-1] if data else 0)


if __name__ == "__main__":
    main()