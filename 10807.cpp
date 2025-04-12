#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, x, v, cnt = 0;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    cin >> v;
    for (int i = 0; i < n; ++i) cnt += (a[i] == v);
    cout << cnt;
}
