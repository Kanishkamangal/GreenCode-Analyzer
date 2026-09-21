// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;

    if (!(cin >> n >> m) || n <= 0 || m < 0)
        return 0;

    vector<vector<int>> adj(n);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;

        if (u >= 0 && u < n &&
            v >= 0 && v < n) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    int source;

    if (!(cin >> source) ||
        source < 0 || source >= n)
        return 0;

    vector<bool> visited(n, false);
    queue<int> q;

    visited[source] = true;
    q.push(source);

    bool first = true;

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        if (!first)
            cout << ' ';

        cout << node;
        first = false;

        for (int next : adj[node]) {
            if (!visited[next]) {
                visited[next] = true;
                q.push(next);
            }
        }
    }

    cout << '\n';

    return 0;
}
