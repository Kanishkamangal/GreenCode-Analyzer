// Benchmark: Character Frequency in String
// Category: Strings
// Algorithm: Linear Character Frequency Count - O(n)

#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    char target;

    if (!(cin >> s)) {
        return 1;
    }

    if (!(cin >> target)) {
        return 1;
    }

    long long frequency = 0;

    for (char ch : s) {
        if (ch == target) {
            frequency++;
        }
    }

    cout
        << frequency
        << '\n';

    return 0;
}
