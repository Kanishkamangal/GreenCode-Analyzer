// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s1, s2;

    if (!(cin >> s1 >> s2)) {
        cout << "0\n";
        return 0;
    }

    if (s1.size() != s2.size()) {
        cout << "0\n";
        return 0;
    }

    long long count[256] = {0};

    for (unsigned char c : s1)
        count[c]++;

    for (unsigned char c : s2)
        count[c]--;

    for (long long value : count) {
        if (value != 0) {
            cout << "0\n";
            return 0;
        }
    }

    cout << "1\n";
    return 0;
}
