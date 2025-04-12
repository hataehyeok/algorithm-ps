#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int n, m; cin >> n >> m;
    while (n--) {
        string s; cin >> s;
        reverse(s.begin(), s.end());
        cout << s << '\n';
    }
}


// ✅ 요약 설명
// 	•	string s에 각 행을 입력받고, reverse()로 뒤집기.
// 	•	바로 출력.

// 🧠 시간 복잡도
// 	•	최대 10행, 10열 → 완전 여유.