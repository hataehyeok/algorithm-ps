#include <stdio.h>
#include <stdlib.h>

int main(){
    int a, b;
    scanf("%d %d", &a, &b);
    if(b<45){
        b = 60+b-45;
        a = a-1;
    }
    else if(b>45){
        b = b-45;
    }
    if(a<0){
        a=24+a;
    }
    printf("%d %d", a, b);
    return 0;
}