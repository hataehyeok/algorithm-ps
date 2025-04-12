#include <stdio.h>

int main() {
    int n, k, p; scanf("%d %d %d", &n, &k, &p);
    int cream;
    int sellable = 0;
    while(n--) {
        int no_cream = 0;
        int k2 = k;
        while(k2--) {
            scanf("%d", &cream);
            if(cream == 0) no_cream++;
        }
        if(no_cream < p) sellable++;
    }
    printf("%d\n", sellable);
    return 0;
}

