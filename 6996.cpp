#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int t; cin >> t;
    cin.ignore();
    while (t--) {
        string line, a, b;
        getline(cin, line);
        istringstream ss(line);
        ss >> a >> b;
        string sa = a, sb = b;
        sort(sa.begin(), sa.end());
        sort(sb.begin(), sb.end());
        cout << a << " & " << b << " are " << (sa == sb ? "" : "NOT ") << "anagrams.\n";
    }
}