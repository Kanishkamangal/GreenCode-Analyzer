// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, m;

    if (scanf("%d %d", &n, &m) != 2 || n <= 0 || m < 0) {
        return 0;
    }

    int *degree = (int *)calloc(n, sizeof(int));
    int *u = (int *)malloc(m * sizeof(int));
    int *v = (int *)malloc(m * sizeof(int));

    for (int i = 0; i < m; i++) {
        scanf("%d %d", &u[i], &v[i]);

        if (u[i] >= 0 && u[i] < n &&
            v[i] >= 0 && v[i] < n) {
            degree[u[i]]++;
            degree[v[i]]++;
        }
    }

    int **adj = (int **)malloc(n * sizeof(int *));
    int *position = (int *)calloc(n, sizeof(int));

    for (int i = 0; i < n; i++) {
        adj[i] = (int *)malloc(degree[i] * sizeof(int));
    }

    for (int i = 0; i < m; i++) {
        if (u[i] >= 0 && u[i] < n &&
            v[i] >= 0 && v[i] < n) {
            adj[u[i]][position[u[i]]++] = v[i];
            adj[v[i]][position[v[i]]++] = u[i];
        }
    }

    int source;

    if (scanf("%d", &source) != 1 ||
        source < 0 || source >= n) {
        return 0;
    }

    int *visited = (int *)calloc(n, sizeof(int));
    int *queue = (int *)malloc(n * sizeof(int));

    int front = 0;
    int rear = 0;

    queue[rear++] = source;
    visited[source] = 1;

    int first = 1;

    while (front < rear) {
        int node = queue[front++];

        if (!first) printf(" ");
        printf("%d", node);
        first = 0;

        for (int i = 0; i < degree[node]; i++) {
            int next = adj[node][i];

            if (!visited[next]) {
                visited[next] = 1;
                queue[rear++] = next;
            }
        }
    }

    printf("\n");

    for (int i = 0; i < n; i++)
        free(adj[i]);

    free(adj);
    free(degree);
    free(position);
    free(u);
    free(v);
    free(visited);
    free(queue);

    return 0;
}
