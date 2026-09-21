// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    string second;

    if (!(cin >> first)) {
        return 1;
    }

    if (!(cin >> second)) {
        return 1;
    }

    int n = (int)first.size();
    int m = (int)second.size();

    vector<int> previous(m + 1, 0);
    vector<int> current(m + 1, 0);

    for (int i = 1; i <= n; i++) {
        current[0] = 0;

        for (int j = 1; j <= m; j++) {
            if (
                first[i - 1] ==
                second[j - 1]
            ) {
                current[j] =
                    previous[j - 1] + 1;
            } else {
                current[j] =
                    max(
                        previous[j],
                        current[j - 1]
                    );
            }
        }

        swap(previous, current);
    }

    cout << previous[m] << '\n';

    return 0;
}
