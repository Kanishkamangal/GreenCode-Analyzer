#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> a;
    long long x;

    while (cin >> x) {
        a.push_back(x);
    }

    int n = static_cast<int>(a.size());

    for (int i = 1; i < n; i++) {
        long long key = a[i];
        int j = i - 1;

        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }

        a[j + 1] = key;
    }

    cout << (a.empty() ? 0 : a.back());

    return 0;
}