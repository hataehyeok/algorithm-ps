#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    while (true) {
        int n, x, prev = -1;
        cin >> n;
        if (!n) break;
        while (n--) {
            cin >> x;
            if (x != prev) {
                cout << x << ' ';
                prev = x;
            }
        }
        cout << "$\n";
    }
}