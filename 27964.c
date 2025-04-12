#include <stdio.h>
#include <string.h>

int main() {
    int n, count = 0;
    char topping[100][101], unique[100][101];
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%s", topping[i]);
    for (int i = 0; i < n; i++) {
        int len = strlen(topping[i]);
        if (len >= 6 && strcmp(&topping[i][len - 6], "Cheese") == 0) {
            char cheese[101];
            strncpy(cheese, topping[i], len - 6);
            cheese[len - 6] = '\0';
            int unique_flag = 1;
            for (int j = 0; j < count; j++) {
                if (strcmp(unique[j], cheese) == 0) {
                    unique_flag = 0;
                    break;
                }
            }
            if (unique_flag) strcpy(unique[count++], cheese);
        }
    }
    printf("%s\n", count >= 4 ? "yummy" : "sad");
    return 0;
}