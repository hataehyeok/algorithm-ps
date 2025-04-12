#include <stdio.h>

int main() {
    int num1, num2;
    scanf("%d %d", &num1, &num2);

    int digit1 = num2 % 10;
    int digit2 = (num2 / 10) % 10;
    int digit3 = num2 / 100;

    int result1 = num1 * digit1;
    int result2 = num1 * digit2;
    int result3 = num1 * digit3;
    int result4 = num1 * num2;

    printf("%d\n", result1);
    printf("%d\n", result2);
    printf("%d\n", result3);
    printf("%d\n", result4);

    return 0;
} 