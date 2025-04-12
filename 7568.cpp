#include <bits/stdc++.h>
using namespace std;

int main() {
    int N; cin >> N;
    vector<pair<int, int>> p(N);
    for (int i = 0; i < N; i++) cin >> p[i].first >> p[i].second;
    for (int i = 0; i < N; i++) {
        int r = 1;
        for (int j = 0; j < N; j++) {
            if (p[i].first < p[j].first && p[i].second < p[j].second) r++;
        }
        cout << r << ' ';
    }
}