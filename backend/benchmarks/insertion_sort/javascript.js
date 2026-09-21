const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

const a = input
    ? input.split(/\s+/).map(Number)
    : [];

const n = a.length;

for (let i = 1; i < n; i++) {
    const key = a[i];
    let j = i - 1;

    while (
        j >= 0 &&
        a[j] > key
    ) {
        a[j + 1] = a[j];
        j--;
    }

    a[j + 1] = key;
}

process.stdout.write(
    String(
        n === 0 ? 0 : a[n - 1]
    )
);
