// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

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

    int left = 0;
    int right = (int)s.size() - 1;
    bool palindrome = true;

    while (left < right) {
        if (s[left] != s[right]) {
            palindrome = false;
            break;
        }

        left++;
        right--;
    }

    cout << (palindrome ? 1 : 0) << '\n';

    return 0;
}
