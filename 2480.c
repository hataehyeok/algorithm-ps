#include <stdio.h>

int main() {
    int a,b,c;
    scanf("%d %d %d", &a, &b, &c);

    if (a==b && b==c) printf("%d\n", 10000 + a*1000);
    else if (a==b || a==c) printf("%d\n", 1000 + a*100);
    else if (b==c) printf("%d\n", 1000 + b*100);
    else {
        int max = a;
        max = max < b ? b : max;
        max = max < c ? c : max;
        printf("%d\n", max*100);
    }
    return 0;
}