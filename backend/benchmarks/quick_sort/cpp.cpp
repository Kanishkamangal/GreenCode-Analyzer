// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

#include <iostream>
#include <vector>
using namespace std;

int partitionArray(
    vector<long long>& a,
    int low,
    int high
) {
    long long pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (a[j] <= pivot) {
            i++;
            swap(a[i], a[j]);
        }
    }

    swap(a[i + 1], a[high]);

    return i + 1;
}

void quickSort(
    vector<long long>& a,
    int low,
    int high
) {
    if (low < high) {
        int pivotIndex = partitionArray(
            a,
            low,
            high
        );

        quickSort(
            a,
            low,
            pivotIndex - 1
        );

        quickSort(
            a,
            pivotIndex + 1,
            high
        );
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
        quickSort(
            a,
            0,
            (int)a.size() - 1
        );
    }

    cout << (a.empty() ? 0 : a.back()) << '\n';

    return 0;
}
