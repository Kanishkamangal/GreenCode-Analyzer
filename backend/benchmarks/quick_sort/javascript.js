// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

const a = input
    ? input.split(/\s+/).map(Number)
    : [];

function partition(
    a,
    low,
    high
) {
    const pivot = a[high];
    let i = low - 1;

    for (let j = low; j < high; j++) {
        if (a[j] <= pivot) {
            i++;

            const temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }

    const temp = a[i + 1];
    a[i + 1] = a[high];
    a[high] = temp;

    return i + 1;
}

function quickSort(
    a,
    low,
    high
) {
    if (low < high) {
        const pivotIndex = partition(
            a,
            low,
            high
        );

        quickSort(
            a,
            low,
            pivotIndex - 1
        );

        quickSort(
            a,
            pivotIndex + 1,
            high
        );
    }
}

if (a.length > 0) {
    quickSort(
        a,
        0,
        a.length - 1
    );
}

console.log(
    a.length === 0 ? 0 : a[a.length - 1]
);
