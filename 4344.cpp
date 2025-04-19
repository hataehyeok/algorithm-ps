#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int C; cin >> C;
    
    while (C--) {
        int N; cin >> N;
        vector<int> scores(N);
        double sum = 0;
        
        for (int i = 0; i < N; i++) {
            cin >> scores[i];
            sum += scores[i];
        }
        
        double avg = sum / N;
        int count = 0;
        
        for (int i = 0; i < N; i++) {
            if (scores[i] > avg) count++;
        }
        
        cout << fixed << setprecision(3) << (count * 100.0) / N << "%" << '\n';
    }
    
    return 0;
}