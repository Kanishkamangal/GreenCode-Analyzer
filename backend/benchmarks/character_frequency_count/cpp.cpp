// Benchmark: Character Frequency Count
// Category: Character
// Algorithm: Linear Frequency Count - O(n)

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

    long long count = 0;

    for (char ch : s) {
        if (ch == target) {
            count++;
        }
    }

    cout << count << '\n';

    return 0;
}
