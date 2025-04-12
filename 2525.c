#include <stdio.h>

int main() {
    int hour, minute, cook_time;
    
    scanf("%d %d", &hour, &minute);
    scanf("%d", &cook_time);
    
    minute += cook_time;
    hour += minute / 60;
    minute %= 60;
    hour %= 24;
    
    printf("%d %d\n", hour, minute);
    
    return 0;
}