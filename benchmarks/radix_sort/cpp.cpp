// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

#include <iostream>
#include <vector>
using namespace std;

void radixSortNonNegative(
    vector<unsigned long long>& a
) {
    if (a.size() <= 1) {
        return;
    }

    unsigned long long maxValue = a[0];

    for (unsigned long long value : a) {
        if (value > maxValue) {
            maxValue = value;
        }
    }

    vector<unsigned long long> output(
        a.size()
    );

    for (
        unsigned long long exp = 1;
        maxValue / exp > 0;
    ) {
        int count[10] = {0};

        for (unsigned long long value : a) {
            int digit =
                (int)((value / exp) % 10);

            count[digit]++;
        }

        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        for (
            int i = (int)a.size() - 1;
            i >= 0;
            i--
        ) {
            int digit =
                (int)((a[i] / exp) % 10);

            output[
                --count[digit]
            ] = a[i];
        }

        a = output;

        if (exp > maxValue / 10) {
            break;
        }

        exp *= 10;
    }
}

void radixSort(
    vector<long long>& a
) {
    vector<unsigned long long> negative;
    vector<unsigned long long> positive;

    for (long long value : a) {
        if (value < 0) {
            negative.push_back(
                0ULL -
                (unsigned long long)value
            );
        } else {
            positive.push_back(
                (unsigned long long)value
            );
        }
    }

    radixSortNonNegative(negative);
    radixSortNonNegative(positive);

    int index = 0;

    for (
        int i = (int)negative.size() - 1;
        i >= 0;
        i--
    ) {
        a[index++] =
            -(long long)negative[i];
    }

    for (
        unsigned long long value : positive
    ) {
        a[index++] =
            (long long)value;
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
        radixSort(a);
    }

    cout
        << (a.empty() ? 0 : a.back())
        << '\n';

    return 0;
}
