// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;

    if (!(cin >> n) || n < 0) {
        return 1;
    }

    vector<long long> a(n);

    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    long long target;
    cin >> target;

    int result = -1;

    for (int i = 0; i < n; i++) {
        if (a[i] == target) {
            result = i;
            break;
        }
    }

    cout << result << '\n';

    return 0;
}
