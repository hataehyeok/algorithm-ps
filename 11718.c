#include <stdio.h>

int main() {
    char a;

    while(scanf("%c", &a) != EOF) {
        printf("%c", a);
    }

    return 0;
}


#include <stdio.h>

int main() {
    char a[1000];

    while(fgets(a, sizeof(a), stdin) != NULL) {
        printf("%s", a);
    }

    return 0;
}