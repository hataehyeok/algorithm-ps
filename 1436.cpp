#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n; cin >> n;
    
    int num = 666, cnt = 0;
    while(cnt < n) {
        int temp = num;
        bool has666 = false;
        int consec6 = 0;
        
        while(temp > 0) {
            if(temp % 10 == 6)
                consec6++;
            else
                consec6 = 0;
                
            if(consec6 >= 3) {
                has666 = true;
                break;
            }
            
            temp /= 10;
        }
        
        if(has666) cnt++;
        if(cnt < n) num++;
    }
    
    cout << num << '\n';
    return 0;
}