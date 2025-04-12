#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    for(int i = n; i > 0; i--){
        int j=i;
        while(j--){
            printf("*");
        }
        printf("\n");
    }
}