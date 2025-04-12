#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int t; cin >> t;
    
    while(t--) {
        int a, b, c; cin >> a >> b >> c;
        
        int cnt = 0;
        for(int x=1; x<=a; x++) {
            for(int y=1; y<=b; y++) {
                for(int z=1; z<=c; z++) {
                    if((x%y) == (y%z) && (y%z) == (z%x))
                        cnt++;
                }
            }
        }
        
        cout << cnt << '\n';
    }
    return 0;
}

// int t; cin>>t; 써서 테케 개수 바로 입력받기
// 테케 개수만큼 반복하는건, while(t--)로 바로 구현하고,
// while 안에서 int a,b,c; cin>>a>>b>>c;하면 바로 iteration에 대한 입력까지 한번에 끝낼 수 있음
