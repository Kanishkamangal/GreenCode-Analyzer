// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

#include <iostream>
#include <vector>
using namespace std;

void shellSort(
    vector<long long>& a
) {
    int n = (int)a.size();

    for (
        int gap = n / 2;
        gap > 0;
        gap /= 2
    ) {
        for (
            int i = gap;
            i < n;
            i++
        ) {
            long long temp = a[i];
            int j = i;

            while (
                j >= gap &&
                a[j - gap] > temp
            ) {
                a[j] = a[j - gap];
                j -= gap;
            }

            a[j] = temp;
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
        shellSort(a);
    }

    cout
        << (a.empty() ? 0 : a.back())
        << '\n';

    return 0;
}
