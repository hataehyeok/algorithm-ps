#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, l; cin >> n >> l;
    
    int cnt = 0, num = 0;
    while(cnt < n) {
        num++;
        int t = num;
        bool valid = true;
        while(t) {
            if(t % 10 == l) {
                valid = false;
                break;
            }
            t /= 10;
        }
        if(valid) cnt++;
    }
    
    cout << num << '\n';
    return 0;
}

// int n, l; cin >> n >> l; 을 써서 첫줄에 입력 받는걸 정의와 동시에 입력 처리
