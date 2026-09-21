// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

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

function heapify(
    a,
    n,
    i
) {
    let largest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;

    if (
        left < n &&
        a[left] > a[largest]
    ) {
        largest = left;
    }

    if (
        right < n &&
        a[right] > a[largest]
    ) {
        largest = right;
    }

    if (largest !== i) {
        const temp = a[i];
        a[i] = a[largest];
        a[largest] = temp;

        heapify(
            a,
            n,
            largest
        );
    }
}

function heapSort(a) {
    const n = a.length;

    for (
        let i = Math.floor(n / 2) - 1;
        i >= 0;
        i--
    ) {
        heapify(
            a,
            n,
            i
        );
    }

    for (
        let i = n - 1;
        i > 0;
        i--
    ) {
        const temp = a[0];
        a[0] = a[i];
        a[i] = temp;

        heapify(
            a,
            i,
            0
        );
    }
}

if (a.length > 0) {
    heapSort(a);
}

console.log(
    a.length === 0
        ? 0
        : a[a.length - 1]
);
