#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n; cin >> n;
    for(int i=1; i<n; i++) {
        int sum = i, tmp = i;
        while(tmp) {
            sum += tmp % 10;
            tmp /= 10;
        }
        if(sum == n) {
            cout << i << '\n';
            return 0;
        }
    }
    cout << 0 << '\n';
    return 0;
}

// 가장 작은 생성자를 출력해야 함
// for 문으로 i부터 시작해서 첫번째 생성자를 찾으면 그게 가장 작은 생성자가 됨
