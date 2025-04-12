#include <bits/stdc++.h>
using namespace std;

bool bpm(int u, vector<vector<int>> &graph, vector<bool> &visited, vector<int> &match) {
    for (int v : graph[u]) {
        if (!visited[v]) {
            visited[v] = true;
            if (match[v] == -1 || bpm(match[v], graph, visited, match)) {
                match[v] = u;
                return true;
            }
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int N; cin >> N;
    vector<vector<int>> graph(N);

    for (int i = 0; i < N; ++i) {
        int Ai; cin >> Ai;
        while (Ai--) {
            int x; cin >> x;
            graph[i].push_back(x - 1);
        }
    }

    vector<int> match(N, -1);
    for (int i = 0; i < N; ++i) {
        vector<bool> visited(N, false);
        if (!bpm(i, graph, visited, match)) {
            cout << -1 << '\n';
            return 0;
        }
    }

    for (int i = 0; i < N; ++i) {
        int assigned = -1;
        for (int j = 0; j < N; ++j) {
            if (match[j] == i) {
                assigned = j;
                break;
            }
        }

        vector<int> temp_match = match;
        temp_match[assigned] = -1;
        vector<bool> visited(N, false);
        bool found = false;
        for (int v : graph[i]) {
            if (v == assigned) continue;
            visited.assign(N, false);
            if (match[v] == -1 || bpm(match[v], graph, visited, temp_match)) {
                found = true;
                break;
            }
        }
        if (found) {
            cout << -1 << '\n';
            return 0;
        }
    }

    vector<int> result(N);
    for (int i = 0; i < N; ++i)
        result[match[i]] = i + 1;

    cout << 1 << '\n';
    for (int x : result) cout << x << ' ';
    cout << '\n';

    return 0;
}
