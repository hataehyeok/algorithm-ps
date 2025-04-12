#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n; cin >> n;
    int board[1001][1001] = {};
    for (int k = 1; k <= n; ++k) {
        int x, y, w, h; cin >> x >> y >> w >> h;
        for (int i = x; i < x + w; ++i)
            for (int j = y; j < y + h; ++j)
                board[i][j] = k;
    }
    vector<int> area(n + 1);
    for (int i = 0; i <= 1000; ++i)
        for (int j = 0; j <= 1000; ++j)
            if (board[i][j]) area[board[i][j]]++;
    for (int i = 1; i <= n; ++i) cout << area[i] << '\n';
}

// ✅ 핵심 전략:
// 	•	격자 board[1001][1001]에 각 칸을 가장 마지막에 덮은 색종이의 번호로 마킹.
// 	•	나중에 한 번 더 전체 격자를 순회하며, 각 번호가 차지하는 칸 수만큼 면적을 센다.

// 💡 설명
// 	•	각 색종이마다 (x, y) 위치에 w x h 직사각형을 그리되,
// 	•	그 칸을 **현재 색종이 번호(k)**로 마킹.
// 	•	나중에 온 색종이가 같은 칸을 덮으면 덮은 번호로 덮임 → 자연스레 가려짐 처리됨.
// 	•	마지막에 전체 1001×1001 격자를 돌며 area[k]++ 해서 각 색종이의 보이는 면적 계산.

// ✅ 시간복잡도
// 	•	색종이당 최대 100×100 = 10,000 칸 → N=100이므로 총 1,000,000 연산 이내 ✅
// 	•	전체 board 한 번 순회 → 1001×1001 = 약 100만 → 시간 여유 있음