// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

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

function shellSort(a) {
    const n = a.length;

    for (
        let gap = Math.floor(n / 2);
        gap > 0;
        gap = Math.floor(gap / 2)
    ) {
        for (
            let i = gap;
            i < n;
            i++
        ) {
            const temp = a[i];
            let j = i;

            while (
                j >= gap &&
                a[j - gap] > temp
            ) {
                a[j] = a[j - gap];
                j -= gap;
            }

            a[j] = temp;
        }
    }
}

if (a.length > 0) {
    shellSort(a);
}

console.log(
    a.length === 0
        ? 0
        : a[a.length - 1]
);
