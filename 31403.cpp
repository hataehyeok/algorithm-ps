#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    string a, b, c; cin >> a >> b >> c;
    cout << stoi(a) + stoi(b) - stoi(c) << '\n';
    cout << stoi(a + b) - stoi(c) << '\n';
}

// ✅ 설명
// 	•	숫자 계산: stoi(a) + stoi(b) - stoi(c)
// 	•	문자열 계산: (a + b)는 문자열 이어붙이기 → 그걸 stoi()로 숫자로 바꾼 뒤 - stoi(c)

// stoi = string to int
// stof = string to float
// stol = string to long
// stod = string to double
