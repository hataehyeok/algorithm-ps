#include <stdio.h>
#include <stdlib.h>

typedef struct { int port, action_number; } Port;

int main() {
    int N, Q, t, x, action_count = 0;
    scanf("%d %d", &N, &Q);
    Port *ports = (Port *)malloc(N * sizeof(Port));
    for (int i = 0; i < N; i++) ports[i] = (Port){i + 1, 0};
    while (Q--) {
        scanf("%d %d", &t, &x);
        if (t == 1) {
            int found = 0;
            for (int j = 0; j < N; j++) {
                if (ports[j].port >= x && ports[j].action_number == 0) {
                    ports[j].action_number = ++action_count;
                    printf("%d\n", ports[j].port);
                    found = 1;
                    break;
                }
            }
            if (!found) printf("-1\n");
        } else {
            int found = 0;
            for (int j = 0; j < N; j++) {
                if (ports[j].port == x && ports[j].action_number != 0) {
                    printf("%d\n", ports[j].action_number);
                    ports[j].action_number = 0;
                    found = 1;
                    break;
                }
            }
            if (!found) printf("-1\n");
        }
    }
    free(ports);
    return 0;
}