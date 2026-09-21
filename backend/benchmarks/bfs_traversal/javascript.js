// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

const fs = require("fs");

const tokens = fs
    .readFileSync(0, "utf8")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map(Number);

if (tokens.length < 2)
    process.exit(0);

const n = tokens[0];
const m = tokens[1];

if (n <= 0 || m < 0)
    process.exit(0);

const adj = Array.from(
    { length: n },
    () => []
);

let index = 2;

for (let i = 0; i < m; i++) {
    if (index + 1 >= tokens.length)
        process.exit(0);

    const u = tokens[index++];
    const v = tokens[index++];

    if (
        u >= 0 && u < n &&
        v >= 0 && v < n
    ) {
        adj[u].push(v);
        adj[v].push(u);
    }
}

if (index >= tokens.length)
    process.exit(0);

const source = tokens[index];

if (source < 0 || source >= n)
    process.exit(0);

const visited = new Array(n).fill(false);
const queue = new Array(n);

let front = 0;
let rear = 0;

queue[rear++] = source;
visited[source] = true;

const result = [];

while (front < rear) {
    const node = queue[front++];

    result.push(node);

    for (const next of adj[node]) {
        if (!visited[next]) {
            visited[next] = true;
            queue[rear++] = next;
        }
    }
}

console.log(result.join(" "));
