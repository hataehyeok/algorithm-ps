#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int m, n; cin >> m >> n;
    
    vector<vector<int>> planets(m, vector<int>(n));
    for(int i=0; i<m; i++)
        for(int j=0; j<n; j++)
            cin >> planets[i][j];
    
    int count = 0;
    for(int i=0; i<m; i++) {
        for(int j=i+1; j<m; j++) {
            bool equal = true;
            
            for(int p=0; p<n; p++) {
                for(int q=0; q<n; q++) {
                    if((planets[i][p] < planets[i][q]) != (planets[j][p] < planets[j][q]) ||
                       (planets[i][p] == planets[i][q]) != (planets[j][p] == planets[j][q]) ||
                       (planets[i][p] > planets[i][q]) != (planets[j][p] > planets[j][q])) {
                        equal = false;
                        break;
                    }
                }
                if(!equal) break;
            }
            
            if(equal) count++;
        }
    }
    
    cout << count << '\n';
    return 0;
}