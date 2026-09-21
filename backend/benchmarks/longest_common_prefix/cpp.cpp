// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;

    if (!(cin >> n) || n <= 0) {
        cout << '\n';
        return 0;
    }

    vector<string> strings(n);

    for (int i = 0; i < n; i++) {
        cin >> strings[i];
    }

    int prefixLength = 0;

    for (
        int position = 0;
        position < (int)strings[0].size();
        position++
    ) {
        char current =
            strings[0][position];

        bool matches = true;

        for (int i = 1; i < n; i++) {
            if (
                position >=
                    (int)strings[i].size() ||
                strings[i][position] != current
            ) {
                matches = false;
                break;
            }
        }

        if (!matches) {
            break;
        }

        prefixLength++;
    }

    for (
        int i = 0;
        i < prefixLength;
        i++
    ) {
        cout << strings[0][i];
    }

    cout << '\n';

    return 0;
}
