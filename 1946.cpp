#include <bits/stdc++.h>
using namespace std;
#define F first
#define S second

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int T; cin >> T;
    while (T--) {
        int N; cin >> N;
        vector<pair<int, int>> applicants(N);
        for (int i = 0; i < N; i++) cin >> applicants[i].F >> applicants[i].S;
        sort(applicants.begin(), applicants.end());
        int count = 0, min_interview_rank = INT_MAX;
        for (auto &[F, S] : applicants) {
            if (S < min_interview_rank) {
                count++;
                min_interview_rank = S;
            }
        }
        cout << count << '\n';
    }
    return 0;
}