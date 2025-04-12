#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);cin.tie(0);
    vector<int> dwarfs(9);
    
    int total = 0;
    for(int i = 0; i < 9; i++) {
        cin >> dwarfs[i];
        total += dwarfs[i];
    }
    
    for(int i = 0; i < 8; i++) {
        for(int j = i + 1; j < 9; j++) {
            if(total - dwarfs[i] - dwarfs[j] == 100) {
                for(int k = 0; k < 9; k++) {
                    if(k != i && k != j) {
                        cout << dwarfs[k] << '\n';
                    }
                }
                return 0;
            }
        }
    }
}