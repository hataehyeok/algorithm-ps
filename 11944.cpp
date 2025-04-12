#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    string n; int m; cin >> n >> m;
    string res;
    for (int i = 0; i < stoi(n) && res.size() < m; ++i) res += n;
    cout << res.substr(0, m);
}

// ✅ 설명
// 	•	n을 문자열로 받아서 바로 res에 n을 반복해서 붙여줌.
// 	•	반복 횟수는 stoi(n) 만큼, 하지만 길이 제한 res.size() < m도 함께 걸어줌 → 낭비 없이 멈춤.
// 	•	마지막에 substr(0, m)으로 원하는 만큼만 출력