#include <bits/stdc++.h>
using namespace std;

struct SegmentTree {
    vector<pair<int, int>> tree;
    int size;

    SegmentTree(int n) {
        size = n;
        tree.resize(4 * n, {INT_MAX, -1});
    }

    void update(int idx, int value, int node, int start, int end) {
        if (start == end) {
            tree[node] = {value, start};
        } else {
            int mid = (start + end) / 2;
            if (idx <= mid) update(idx, value, 2 * node, start, mid);
            else update(idx, value, 2 * node + 1, mid + 1, end);

            tree[node] = min(tree[2 * node], tree[2 * node + 1]);
        }
    }

    pair<int, int> query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return {INT_MAX, -1};
        if (l <= start && end <= r) return tree[node];

        int mid = (start + end) / 2;
        return min(query(2 * node, start, mid, l, r), query(2 * node + 1, mid + 1, end, l, r));
    }

    void update(int idx, int value) {
        update(idx, value, 1, 0, size - 1);
    }

    pair<int, int> query(int l, int r) {
        return query(1, 0, size - 1, l, r);
    }
};

int main() {
    ios::sync_with_stdio(0); cin.tie(0);

    int n, m; cin >> n >> m;
    vector<int> A(n + 1), B(m + 1);
    set<pair<int, int>> sa, sb;

    for (int i = 1; i <= n; ++i) {
        cin >> A[i];
        sa.insert({A[i], i});
    }
    for (int i = 1; i <= m; ++i) {
        cin >> B[i];
        sb.insert({B[i], i});
    }

    int k; cin >> k;
    while (k--) {
        string cmd; cin >> cmd;
        if (cmd == "U") {
            int x, y; cin >> x >> y;
            if (x <= n) {
                sa.erase({A[x], x});
                A[x] = y;
                sa.insert({A[x], x});
            } else {
                x -= n;
                sb.erase({B[x], x});
                B[x] = y;
                sb.insert({B[x], x});
            }
        } else { // L
            auto [va, ia] = *sa.begin();
            auto [vb, ib] = *sb.begin();
            cout << ia << ' ' << ib + n << '\n';
        }
    }
}