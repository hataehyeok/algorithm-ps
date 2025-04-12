#include <stdio.h>

int main() {
    int A, B;   
    while (scanf("%d %d", &A, &B) == 2) {
        printf("%d\n", A + B);
    }
    
    return 0;
}
// scanf는 성공적으로 읽은 항목의 수를 반환
// 파일의 끝(EOF)에 도달하면 EOF(-1)를 반환