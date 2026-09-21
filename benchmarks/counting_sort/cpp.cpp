// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

#include <iostream>
#include <vector>
using namespace std;

void countingSort(
    vector<long long>& a
) {
    if (a.size() <= 1) {
        return;
    }

    long long minValue = a[0];
    long long maxValue = a[0];

    for (long long value : a) {
        if (value < minValue) {
            minValue = value;
        }

        if (value > maxValue) {
            maxValue = value;
        }
    }

    long long range =
        maxValue - minValue + 1;

    vector<long long> count(
        (size_t)range,
        0
    );

    for (long long value : a) {
        count[
            (size_t)(value - minValue)
        ]++;
    }

    int index = 0;

    for (
        long long i = 0;
        i < range;
        i++
    ) {
        while (count[(size_t)i] > 0) {
            a[index++] =
                i + minValue;

            count[(size_t)i]--;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> a;
    long long x;

    while (cin >> x) {
        a.push_back(x);
    }

    if (!a.empty()) {
        countingSort(a);
    }

    cout
        << (a.empty() ? 0 : a.back())
        << '\n';

    return 0;
}
