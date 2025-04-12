#include <stdio.h>

int main() {
    int A, B, C, N;
    scanf("%d %d %d %d", &A, &B, &C, &N);

    for (int i = 0; i <= N/A; i++) {
        for (int j = 0; j <= N/B; j++) {
            for (int k = 0; k <= N/C; k++) {
                if (i*A + j*B + k*C == N) {
                    printf("1\n");
                    return 0;
                }
            }
        }
    }

    printf("0\n");
    return 0;
}
