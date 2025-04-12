#include <stdio.h>

int main() {
    int N, count = 0;
    scanf("%d", &N);
    
    for (int i = 1; i <= N; i++) {
        int num = i, sum = 0;
        while (num > 0) {
            sum += num % 10;
            num /= 10;
        }
        if (i % sum == 0) count++;
    }
    
    printf("%d\n", count);
    return 0;
}