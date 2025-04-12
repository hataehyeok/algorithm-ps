#include <stdio.h>

int main() {
    int N;
    scanf("%d", &N);

    int scores[N];
    int max_score = 0;
    double sum = 0.0;

    for (int i = 0; i < N; i++) {
        scanf("%d", &scores[i]);
        if (scores[i] > max_score) {
            max_score = scores[i];
        }
    }

    for (int i = 0; i < N; i++) {
        sum += (double)scores[i] / max_score * 100;
    }

    printf("%.6f\n", sum / N);
    return 0;
}