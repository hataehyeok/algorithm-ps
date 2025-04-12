#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    string s; cin >> s;
    int cnt[26] = {};
    for (char c : s) cnt[c - 'a']++;
    for (int i = 0; i < 26; ++i) cout << cnt[i] << ' ';
}



// ✅ 설명
// 	•	cnt[26]: 알파벳 개수만큼 배열.
// 	•	'a'는 인덱스 0, 'b'는 1, …, 'z'는 25 → c - 'a'로 인덱싱.
// 	•	마지막엔 공백으로 구분된 26개의 개수 출력.

// 🧠 시간 복잡도
// 	•	O(N) — 최대 길이 100 → 전혀 문제 없음.


// 이 방식은 문자열 빈도 문제에서 자주 쓰이는 전형적인 패턴
// 카운팅 응용 문제나 정렬/해시 기반 문제에도 적용가능