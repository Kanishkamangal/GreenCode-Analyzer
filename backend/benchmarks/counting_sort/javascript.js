// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

const fs = require("fs");

const input = fs
    .readFileSync(
        0,
        "utf8"
    )
    .trim();

const a = input
    ? input
        .split(/\s+/)
        .map(Number)
    : [];

function countingSort(a) {
    if (a.length <= 1) {
        return;
    }

    let minValue = a[0];
    let maxValue = a[0];

    for (const value of a) {
        if (value < minValue) {
            minValue = value;
        }

        if (value > maxValue) {
            maxValue = value;
        }
    }

    const range =
        maxValue - minValue + 1;

    const count =
        new Array(range).fill(0);

    for (const value of a) {
        count[
            value - minValue
        ]++;
    }

    let index = 0;

    for (
        let i = 0;
        i < range;
        i++
    ) {
        while (count[i] > 0) {
            a[index++] =
                i + minValue;

            count[i]--;
        }
    }
}

if (a.length > 0) {
    countingSort(a);
}

console.log(
    a.length === 0
        ? 0
        : a[a.length - 1]
);
