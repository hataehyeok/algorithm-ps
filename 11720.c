#include <stdio.h>

int main() {
    int n, sum = 0;
    scanf("%d", &n);

    while(n--) {
        int num;
        scanf("%d", &num);
        int d = num % 10;
        sum += d;
        num /= 10;
    }

    printf("%d\n", sum);
    return 0;
}