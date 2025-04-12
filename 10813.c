#include <stdio.h>

int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    
    int basket[101];
    for(int i=1; i<=n; i++) {
        basket[i] = i;
    }
    
    for(int k=0; k<m; k++) {
        int i, j;
        scanf("%d %d", &i, &j);
        
        int temp = basket[i];
        basket[i] = basket[j];
        basket[j] = temp;
    }
    
    for(int i=1; i<=n; i++) {
        printf("%d ", basket[i]);
    }
    
    return 0;
}