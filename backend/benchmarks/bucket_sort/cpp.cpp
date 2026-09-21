// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

void insertionSort(
    vector<long long>& bucket
) {
    for (
        int i = 1;
        i < (int)bucket.size();
        i++
    ) {
        long long key = bucket[i];
        int j = i - 1;

        while (
            j >= 0 &&
            bucket[j] > key
        ) {
            bucket[j + 1] = bucket[j];
            j--;
        }

        bucket[j + 1] = key;
    }
}

void bucketSort(
    vector<long long>& a
) {
    int n = (int)a.size();

    if (n <= 1) {
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

    if (minValue == maxValue) {
        return;
    }

    int bucketCount =
        max(
            1,
            (int)sqrt((double)n)
        );

    vector<vector<long long>> buckets(
        bucketCount
    );

    long double range =
        (long double)maxValue -
        (long double)minValue + 1.0L;

    for (long long value : a) {
        long double offset =
            (long double)value -
            (long double)minValue;

        int index = (int)(
            (offset * bucketCount) /
            range
        );

        if (index >= bucketCount) {
            index = bucketCount - 1;
        }

        buckets[index].push_back(
            value
        );
    }

    int position = 0;

    for (auto& bucket : buckets) {
        insertionSort(bucket);

        for (long long value : bucket) {
            a[position++] = value;
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
        bucketSort(a);
    }

    cout
        << (a.empty() ? 0 : a.back())
        << '\n';

    return 0;
}
