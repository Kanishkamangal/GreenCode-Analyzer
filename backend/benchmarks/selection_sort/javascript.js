const fs = require("fs");

const input = fs.readFileSync(0, "utf8").trim();

const a = input
    ? input.split(/\s+/).map(Number)
    : [];

const n = a.length;

for (let i = 0; i < n - 1; i++) {
    let minIndex = i;

    for (let j = i + 1; j < n; j++) {
        if (a[j] < a[minIndex])
            minIndex = j;
    }

    if (minIndex !== i) {
        const temp = a[i];
        a[i] = a[minIndex];
        a[minIndex] = temp;
    }
}

process.stdout.write(String(n === 0 ? 0 : a[n - 1]));
