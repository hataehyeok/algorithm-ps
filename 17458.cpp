#include <bits/stdc++.h>
using namespace std;

int k, n;
vector<int> base;

set<int> closure(set<int> s) {
    bool changed = true;
    while (changed) {
        changed = false;
        vector<int> v(s.begin(), s.end());
        for (int i = 0; i < v.size(); ++i) {
            for (int j = 0; j < v.size(); ++j) {
                int a = v[i] & v[j], b = v[i] | v[j];
                if (!s.count(a)) s.insert(a), changed = true;
                if (!s.count(b)) s.insert(b), changed = true;
            }
        }
    }
    return s;
}

bool is_good(const vector<int>& v) {
    for (int i = 0; i < v.size(); ++i)
        for (int j = 0; j < v.size(); ++j) {
            int a = v[i] & v[j], b = v[i] | v[j];
            if (!count(v.begin(), v.end(), a) || !count(v.begin(), v.end(), b))
                return false;
        }
    return true;
}

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    cin >> k >> n;
    set<int> s;
    for (int i = 0; i < n; ++i) {
        int x; cin >> x;
        s.insert(x);
    }

    set<int> full = closure(s);
    vector<int> elems(full.begin(), full.end());
    int m = elems.size(), cnt = 0;

    for (int mask = 1; mask < (1 << m); ++mask) {
        vector<int> subset;
        bool valid = true;
        for (int i = 0; i < m; ++i)
            if (mask & (1 << i)) subset.push_back(elems[i]);
        for (int x : s)
            if (!count(subset.begin(), subset.end(), x)) {
                valid = false;
                break;
            }

        if (valid && is_good(subset)) cnt++;
    }

    cout << cnt << '\n';
}