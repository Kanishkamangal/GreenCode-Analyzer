// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

int jumpSearch(
    const vector<long long>& a,
    long long target
) {
    int n = (int)a.size();

    if (n == 0) {
        return -1;
    }

    int step =
        max(
            1,
            (int)sqrt((double)n)
        );

    int previous = 0;
    int current = step;

    while (
        previous < n &&
        a[min(current, n) - 1] < target
    ) {
        previous = current;
        current += step;

        if (previous >= n) {
            return -1;
        }
    }

    int end =
        min(current, n);

    for (
        int i = previous;
        i < end;
        i++
    ) {
        if (a[i] == target) {
            return i;
        }

        if (a[i] > target) {
            break;
        }
    }

    return -1;
}

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

    cout
        << jumpSearch(a, target)
        << '\n';

    return 0;
}
