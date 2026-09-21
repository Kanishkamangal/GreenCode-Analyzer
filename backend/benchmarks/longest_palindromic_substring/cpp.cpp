// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;

    if (!(cin >> s)) {
        return 1;
    }

    int n = (int)s.size();
    int bestStart = 0;
    int bestLength = 1;

    for (int center = 0; center < n; center++) {
        int left = center;
        int right = center;

        while (
            left >= 0 &&
            right < n &&
            s[left] == s[right]
        ) {
            int length =
                right - left + 1;

            if (length > bestLength) {
                bestStart = left;
                bestLength = length;
            }

            left--;
            right++;
        }

        left = center;
        right = center + 1;

        while (
            left >= 0 &&
            right < n &&
            s[left] == s[right]
        ) {
            int length =
                right - left + 1;

            if (length > bestLength) {
                bestStart = left;
                bestLength = length;
            }

            left--;
            right++;
        }
    }

    cout
        << s.substr(
            bestStart,
            bestLength
        )
        << '\n';

    return 0;
}
