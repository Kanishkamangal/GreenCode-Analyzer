// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

const a = input
    ? input.split(/\s+/).map(Number)
    : [];

function radixSortNonNegative(a) {
    if (a.length <= 1) {
        return;
    }

    let maxValue = a[0];

    for (const value of a) {
        if (value > maxValue) {
            maxValue = value;
        }
    }

    const output =
        new Array(a.length);

    for (
        let exp = 1;
        Math.floor(maxValue / exp) > 0;
        exp *= 10
    ) {
        const count =
            new Array(10).fill(0);

        for (const value of a) {
            const digit =
                Math.floor(value / exp) % 10;

            count[digit]++;
        }

        for (let i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        for (
            let i = a.length - 1;
            i >= 0;
            i--
        ) {
            const digit =
                Math.floor(a[i] / exp) % 10;

            output[
                --count[digit]
            ] = a[i];
        }

        for (
            let i = 0;
            i < a.length;
            i++
        ) {
            a[i] = output[i];
        }
    }
}

function radixSort(a) {
    const negative = [];
    const positive = [];

    for (const value of a) {
        if (value < 0) {
            negative.push(-value);
        } else {
            positive.push(value);
        }
    }

    radixSortNonNegative(negative);
    radixSortNonNegative(positive);

    let index = 0;

    for (
        let i = negative.length - 1;
        i >= 0;
        i--
    ) {
        a[index++] = -negative[i];
    }

    for (const value of positive) {
        a[index++] = value;
    }
}

if (a.length > 0) {
    radixSort(a);
}

console.log(
    a.length === 0
        ? 0
        : a[a.length - 1]
);
