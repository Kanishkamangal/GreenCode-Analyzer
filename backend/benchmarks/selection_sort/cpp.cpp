#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> a;
    long long x;

    while (cin >> x)
        a.push_back(x);

    int n = a.size();

    for (int i = 0; i < n - 1; i++) {
        int minIndex = i;

        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[minIndex])
                minIndex = j;
        }

        if (minIndex != i)
            swap(a[i], a[minIndex]);
    }

    cout << (a.empty() ? 0 : a.back());
    return 0;
}
