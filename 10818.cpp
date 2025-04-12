#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    
    int n;
    cin >> n;
    
    int min_val = INT_MAX;
    int max_val = INT_MIN;
    int num;
    
    for (int i = 0; i < n; i++) {
        cin >> num;
        min_val = min(min_val, num);
        max_val = max(max_val, num);
    }
    
    cout << min_val << ' ' << max_val;
}