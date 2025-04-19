#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int M, N; cin >> M >> N;
    
    int sum = 0;
    int min_val = -1;
    
    int start = 1;
    while (start * start < M) start++;
    
    for (int i = start; i * i <= N; i++) {
        if (min_val == -1) min_val = i * i;
        sum += i * i;
    }
    
    if (min_val == -1) cout << -1 << '\n';
    else {
        cout << sum << '\n' << min_val << '\n';

    }
    
    return 0;
}