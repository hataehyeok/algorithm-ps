#include <bits/stdc++.h>
using namespace std;
int N, U[1000], ans;
set<int> sums;
int main() {
    cin >> N;
    for (int i = 0; i < N; i++) cin >> U[i];
    sort(U, U + N);
    for (int i = 0; i < N; i++) for (int j = i; j < N; j++) sums.insert(U[i] + U[j]);
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
        int diff = U[i] - U[j];
        if (sums.count(diff)) ans = max(ans, U[i]);
    }
    cout << ans;
}