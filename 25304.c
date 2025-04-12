#include <stdio.h>

int main() {
    int X, N; scanf("%d %d", &X, &N);
    int total = 0;
    while(N--) {
        int price, quantity;
        scanf("%d %d", &price, &quantity);
        total += price * quantity;
    }
    
    if(total == X) printf("Yes\n");
    else printf("No\n");
        
    return 0;
}