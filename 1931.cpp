#include <bits/stdc++.h>
using namespace std;
#define F first
#define S second

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int N; cin >> N;

    vector<pair<int, int>> meetings(N);
    for (int i = 0; i < N; i++) {
        cin >> meetings[i].S >> meetings[i].F;
    }

    sort(meetings.begin(), meetings.end());

    int count = 0, last_end_time = 0;
    for (int i = 0; i < N; i++) {
        if (meetings[i].S >= last_end_time) {
            count++;
            last_end_time = meetings[i].F;
        }
    }

    cout << count << '\n';
    return 0;
}