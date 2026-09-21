// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

#include <iostream>
#include <string>
using namespace std;

int substringSearch(
    const string& text,
    const string& pattern
) {
    int n = (int)text.size();
    int m = (int)pattern.size();

    if (m == 0) {
        return 0;
    }

    if (m > n) {
        return -1;
    }

    for (int i = 0; i <= n - m; i++) {
        int j = 0;

        while (
            j < m &&
            text[i + j] == pattern[j]
        ) {
            j++;
        }

        if (j == m) {
            return i;
        }
    }

    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string text;
    string pattern;

    if (!(cin >> text)) {
        return 1;
    }

    if (!(cin >> pattern)) {
        return 1;
    }

    cout
        << substringSearch(
            text,
            pattern
        )
        << '\n';

    return 0;
}
