// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

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

    while (left < right) {
        char temp = s[left];
        s[left] = s[right];
        s[right] = temp;

        left++;
        right--;
    }

    cout << s << '\n';

    return 0;
}
