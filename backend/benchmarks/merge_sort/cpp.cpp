// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

#include <iostream>
#include <vector>
using namespace std;

void mergeArrays(
    vector<long long>& a,
    int left,
    int mid,
    int right
) {
    vector<long long> temp;

    int i = left;
    int j = mid + 1;

    while (i <= mid && j <= right) {
        if (a[i] <= a[j]) {
            temp.push_back(a[i]);
            i++;
        } else {
            temp.push_back(a[j]);
            j++;
        }
    }

    while (i <= mid) {
        temp.push_back(a[i]);
        i++;
    }

    while (j <= right) {
        temp.push_back(a[j]);
        j++;
    }

    for (int k = 0; k < (int)temp.size(); k++) {
        a[left + k] = temp[k];
    }
}

void mergeSort(
    vector<long long>& a,
    int left,
    int right
) {
    if (left >= right) {
        return;
    }

    int mid = left + (right - left) / 2;

    mergeSort(a, left, mid);
    mergeSort(a, mid + 1, right);

    mergeArrays(a, left, mid, right);
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
        mergeSort(
            a,
            0,
            (int)a.size() - 1
        );
    }

    cout << (a.empty() ? 0 : a.back()) << '\n';

    return 0;
}
