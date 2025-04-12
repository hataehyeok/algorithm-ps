#include <stdio.h>

int count_claps(int num) {
    int count = 0;
    while (num > 0) {
        int digit = num % 10;
        if (digit == 3 || digit == 6 || digit == 9) {
            count++;
        }
        num /= 10;
    }
    return count;
}

int main() {
    int N, total_claps = 0;
    scanf("%d", &N);

    for (int i = 1; i <= N; i++) {
        total_claps += count_claps(i);
    }

    printf("%d\n", total_claps);
    return 0;
}