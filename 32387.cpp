#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int N, Q; cin >> N >> Q;
    set<int> available_ports;
    vector<int> port_status(N + 1, -1);
    vector<int> action_time(N + 1, -1);

    for (int i = 1; i <= N; ++i) available_ports.insert(i);

    int current_time = 0;
    while (Q--) {
        int t, i; cin >> t >> i;
        ++current_time;

        if (t == 1) {
            auto it = available_ports.lower_bound(i);
            if (it == available_ports.end()) {
                cout << -1 << '\n';
            } else {
                int port = *it;
                available_ports.erase(it);
                port_status[port] = current_time;
                cout << port << '\n';
            }
        } else if (t == 2) {
            if (port_status[i] != -1) {
                cout << port_status[i] << '\n';
                port_status[i] = -1;
                available_ports.insert(i);
            } else {
                cout << -1 << '\n';
            }
        }
    }

    return 0;
}