#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int Q; cin >> Q;
    multiset<int> books;

    while (Q--) {
        int type; cin >> type;
        if (type == 1) {
            int S; cin >> S;
            books.insert(S);
        } else if (type == 2) {
            int S; cin >> S;
            auto it = books.find(S);
            if (it != books.end()) books.erase(it);
        } else if (type == 3) {
            if (books.empty()) {
                cout << 0 << '\n';
                continue;
            }

            int pages = 0;
            auto it = books.begin();
            while (it != books.end()) {
                int current = *it;
                ++pages;
                it = books.upper_bound(current * 2 - 1);
            }

            cout << pages << '\n';
        }
    }

    return 0;
}