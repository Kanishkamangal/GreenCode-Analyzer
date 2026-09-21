// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    char ch;

    if (!(cin >> ch)) {
        return 1;
    }

    bool vowel =
        ch == 'a' ||
        ch == 'e' ||
        ch == 'i' ||
        ch == 'o' ||
        ch == 'u' ||
        ch == 'A' ||
        ch == 'E' ||
        ch == 'I' ||
        ch == 'O' ||
        ch == 'U';

    cout << (vowel ? 1 : 0) << '\n';

    return 0;
}
