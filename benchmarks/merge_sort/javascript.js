// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

const a = input
    ? input.split(/\s+/).map(Number)
    : [];

function merge(a, temp, left, mid, right) {
    let i = left;
    let j = mid + 1;
    let k = left;

    while (i <= mid && j <= right) {
        if (a[i] <= a[j]) {
            temp[k++] = a[i++];
        } else {
            temp[k++] = a[j++];
        }
    }

    while (i <= mid) {
        temp[k++] = a[i++];
    }

    while (j <= right) {
        temp[k++] = a[j++];
    }

    for (let index = left; index <= right; index++) {
        a[index] = temp[index];
    }
}

function mergeSort(a, temp, left, right) {
    if (left >= right) {
        return;
    }

    const mid = Math.floor(
        left + (right - left) / 2
    );

    mergeSort(a, temp, left, mid);
    mergeSort(a, temp, mid + 1, right);

    merge(a, temp, left, mid, right);
}

if (a.length > 0) {
    const temp = new Array(a.length);

    mergeSort(
        a,
        temp,
        0,
        a.length - 1
    );
}

console.log(
    a.length === 0 ? 0 : a[a.length - 1]
);
