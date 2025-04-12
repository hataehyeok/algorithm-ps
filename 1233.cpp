#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);cin.tie(0);
    int s1, s2, s3; cin>>s1>>s2>>s3;
    int sum[81] = {0};

    for(int i=1;i<=s1;i++){
        for(int j=1;j<=s2;j++){
            for(int k=1;k<=s3;k++){
                sum[i+j+k]++;
            }
        }
    }
    int ans = 0;
    for(int i=0;i<81;i++){
        if(sum[i] > sum[ans]){
            ans = i;
        }
    }
    cout<<ans<<"\n";
    return 0;
}