// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, capacity;

    if (!(cin >> n >> capacity) ||
        n < 0 || capacity < 0)
        return 0;

    vector<int> weights(n);
    vector<long long> values(n);

    for (int i = 0; i < n; i++)
        cin >> weights[i];

    for (int i = 0; i < n; i++)
        cin >> values[i];

    vector<long long> dp(
        capacity + 1,
        0
    );

    for (int i = 0; i < n; i++) {
        int weight = weights[i];
        long long value = values[i];

        if (weight <= 0)
            continue;

        for (int c = capacity; c >= weight; c--) {
            dp[c] = max(
                dp[c],
                dp[c - weight] + value
            );
        }
    }

    cout << dp[capacity] << '\n';

    return 0;
}
