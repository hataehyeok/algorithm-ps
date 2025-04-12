#include <bits/stdc++.h>
using namespace std;
#define F first
#define S second
int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int N, c = 1e9;
    cin >> N;
    vector<pair<int, int>> v(N);
    for (int i = 0; i < N; i++) cin >> v[i].F >> v[i].S;
    sort(v.begin(), v.end(), [](pair<int, int> &a, pair<int, int> &b) { return a.S > b.S; });
    for (int i = 0; i < N; i++) c = min(c, v[i].S) - v[i].F;
    cout << (c < 0 ? -1 : c) << '\n';
}