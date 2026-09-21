// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

const a = input
    ? input.split(/\s+/).map(Number)
    : [];

function insertionSort(bucket) {
    for (
        let i = 1;
        i < bucket.length;
        i++
    ) {
        const key = bucket[i];
        let j = i - 1;

        while (
            j >= 0 &&
            bucket[j] > key
        ) {
            bucket[j + 1] =
                bucket[j];

            j--;
        }

        bucket[j + 1] = key;
    }
}

function bucketSort(a) {
    const n = a.length;

    if (n <= 1) {
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

    if (minValue === maxValue) {
        return;
    }

    const bucketCount = Math.max(
        1,
        Math.floor(Math.sqrt(n))
    );

    const buckets =
        Array.from(
            { length: bucketCount },
            () => []
        );

    const range =
        maxValue - minValue + 1;

    for (const value of a) {
        let index = Math.floor(
            (value - minValue) *
            bucketCount /
            range
        );

        if (index >= bucketCount) {
            index =
                bucketCount - 1;
        }

        buckets[index].push(value);
    }

    let position = 0;

    for (const bucket of buckets) {
        insertionSort(bucket);

        for (const value of bucket) {
            a[position++] = value;
        }
    }
}

if (a.length > 0) {
    bucketSort(a);
}

console.log(
    a.length === 0
        ? 0
        : a[a.length - 1]
);
