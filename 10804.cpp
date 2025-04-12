#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    
    vector<int> cards(21);
    for(int i=1; i<=20; i++) cards[i] = i;
    
    for(int i=0; i<10; i++) {
        int a, b; cin >> a >> b;
        reverse(cards.begin()+a, cards.begin()+b+1);
    }
    
    for(int i=1; i<=20; i++)
        cout << cards[i] << (i==20 ? '\n' : ' ');
    
    return 0;
}