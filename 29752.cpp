#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);

    int n, x, cur = 0, ans = 0;
    cin >> n;
    while (n--) {
        cin >> x;
        if (x) cur++;
        else cur = 0;
        ans = max(ans, cur);
    }
    cout << ans;
}