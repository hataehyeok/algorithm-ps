#include <bits/stdc++.h>
using namespace std;

vector<int> p, t[100001];
void dfs(int n) {
    for (int c : t[n]) if (!p[c]) p[c] = n, dfs(c);
}
int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, u, v; cin >> n; p.resize(n + 1);
    for (int i = 1; i < n; ++i) cin >> u >> v, t[u].push_back(v), t[v].push_back(u);
    dfs(1);
    for (int i = 2; i <= n; ++i) cout << p[i] << '\n';
}