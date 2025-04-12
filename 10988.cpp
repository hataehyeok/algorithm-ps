#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    string s; cin >> s;
    string t = s; reverse(t.begin(), t.end());
    cout << (s == t) << '\n';
}