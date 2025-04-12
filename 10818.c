#include <stdio.h>

int main() {
    int n, num, min_val, max_val;
    scanf("%d", &n);
    scanf("%d", &num);
    min_val = max_val = num;
    for (int i = 1; i < n; i++) {
        scanf("%d", &num);
        if (num < min_val) min_val = num;
        if (num > max_val) max_val = num;
    }
    printf("%d %d", min_val, max_val);
    return 0;
}