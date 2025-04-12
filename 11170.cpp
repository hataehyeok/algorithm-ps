#include <iostream>
#include <string>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0); cin.tie(0);
    int t, n, m;
    cin >> t;
    while(t--) {
        cin >> n >> m;
        int ans = 0;
        for(int i = n; i <= m; i++) {
            string s = to_string(i);
            for(char c : s)
                if(c == '0') ans++;
        }
        cout << ans << '\n';
    }
    return 0;
}