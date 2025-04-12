#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, k, mx = 0; cin >> n >> k;
    
    for(int i=1; i<=k; i++) {
        int x = n*i, r = 0;
        while(x) {
            r = r*10 + x%10;
            x /= 10;
        }
        mx = max(mx, r);
    }
    
    cout << mx << '\n';
    return 0;
}


#include<stdio.h>
int main()
{
        int a[7]={0},n,k,g=0,c=0;
        scanf("%d %d",&n,&k);
        for(int i=1;i<=k;i++)
        {
                a[0]=n*k;
                int r=0;
                while(a[0])
                {
                        r=r*10+a[0]%10;
                        a[0]/=10;
                }
                if(g<r) g=r;
        }
        printf("%d",g);
        
        
}