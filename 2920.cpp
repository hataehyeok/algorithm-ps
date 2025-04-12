#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    vector<int> v(8);
    for (int &x : v) cin >> x;

    if (v == vector<int>{1,2,3,4,5,6,7,8}) cout << "ascending";
    else if (v == vector<int>{8,7,6,5,4,3,2,1}) cout << "descending";
    else cout << "mixed";
}


// •	입력을 vector<int> v(8)로 받고, 간단히 == 연산자를 통해 미리 정의한 오름차순/내림차순 벡터와 비교합니다.
// •	모두 다르면 “mixed” 출력.