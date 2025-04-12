#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int sum = 0, best = 0, x;
    for (int i = 0; i < 10; ++i) {
        cin >> x;
        sum += x;
        if (abs(100 - sum) <= abs(100 - best)) best = sum;
    }
    cout << best;
}
