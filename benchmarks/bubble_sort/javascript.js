// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

'use strict';

const fs = require('fs');

const input = fs.readFileSync(0, 'utf8').trim();

const a = input.length === 0
    ? []
    : input.split(/\s+/).map(Number);

for (let i = 0; i < a.length - 1; i++) {

    let swapped = false;

    for (let j = 0; j < a.length - i - 1; j++) {

        if (a[j] > a[j + 1]) {

            const temp = a[j];
            a[j] = a[j + 1];
            a[j + 1] = temp;

            swapped = true;
        }
    }

    if (!swapped) {
        break;
    }
}

console.log(a.length === 0 ? 0 : a[a.length - 1]);