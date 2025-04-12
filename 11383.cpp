#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, m; cin >> n >> m;
    vector<string> a(n), b(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    for (int i = 0; i < n; ++i) cin >> b[i];

    for (int i = 0; i < n; ++i) {
        string doubled;
        for (char c : a[i]) doubled += string(2, c);
        if (doubled != b[i]) {
            cout << "Not Eyfa";
            return 0;
        }
    }
    cout << "Eyfa";
}