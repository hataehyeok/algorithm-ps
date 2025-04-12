#include <stdio.h>
int main() {
    int n, x = 0; 
    scanf("%d %d", &n, &x);
    
    int num[10001];
    for(int i = 0; i < n; i++){
        scanf("%d", &num[i]);
    }
    
    for(int i = 0; i < n; i++){
        if(num[i] < x){
            printf("%d ", num[i]);
        }
    }
    printf("\n");
    
    return 0;
}