#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int t; cin >> t;
    while (t--) {
        string x; cin >> x;
        cout << set<char>(x.begin(), x.end()).size() << '\n';
    }
}

	// •	입력받은 수 X를 문자열로 읽어서 set<char>에 넣으면 자동으로 중복 제거됨.
	// •	set.size()가 바로 아름다운 정도.
	// •	string으로 입력받아서 자릿수별로 쉽게 처리함.