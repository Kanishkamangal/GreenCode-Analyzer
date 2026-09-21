// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

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

    int left = 0;
    int right = n - 1;
    int result = -1;

    while (left <= right) {
        int mid =
            left + (right - left) / 2;

        if (a[mid] == target) {
            result = mid;
            break;
        }

        if (a[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    cout << result << '\n';

    return 0;
}
