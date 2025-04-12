#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, p, q; cin >> n >> p >> q;
    
    vector<int> a(n), b(n), ops(n);
    for(int i=0; i<n; i++) cin >> a[i];
    for(int i=0; i<n; i++) cin >> b[i];
    
    for(int i=0; i<n; i++) {
        int d = a[i] - b[i];
        
        if(p == q) {
            if(d) { cout << "NO\n"; return 0; }
            ops[i] = 0;
            continue;
        }
        
        if(d % (p-q) != 0) { cout << "NO\n"; return 0; }
        
        int k = -d / (p-q);
        if(k < 0 || k > 10000) { cout << "NO\n"; return 0; }
        
        ops[i] = k;
    }
    
    cout << "YES\n";
    for(int i=0; i<n; i++)
        cout << ops[i] << (i == n-1 ? '\n' : ' ');
    
    return 0;
}