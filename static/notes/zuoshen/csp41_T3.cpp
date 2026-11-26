#include <bits/stdc++.h>
using namespace std;

// 大内存容量
const long long MEM_MAX = 1e10;
// 实际内存用动态分配区间即可

// 队列信息
struct Interface {
    int l, r;      // 区间[l, r]
    int head;      // 队首指针（下一个进队的位置，0-based）
    Interface(int l_, int r_): l(l_), r(r_), head(0) {}
};

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n, q;
    cin >> n >> q;

    // 内存管理：维护所有空闲区间，按左端点升序
    // 初始区间[0, 1e10-1]
    using pii = pair<long long, long long>;
    set<pii> freeSeg;
    freeSeg.insert({0, (long long)1e10 - 1});

    // 每个进程的所有接口
    vector<vector<Interface>> proc(n + 1);

    while(q--) {
        string cmd;
        cin >> cmd;
        if(cmd == "new") {
            int p, L;
            cin >> p >> L;
            // 枚举最优段：长度≥L且尽量短/再左
            long long chose_l = -1, chose_r = -1, bestlen = LLONG_MAX;
            for(auto it = freeSeg.begin(); it != freeSeg.end(); ++it) {
                long long l = it->first, r = it->second;
                if(r - l + 1 >= L) {
                    long long cur_len = r - l + 1;
                    if(cur_len < bestlen || (cur_len == bestlen && l < chose_l)) {
                        chose_l = l;
                        chose_r = l+L-1;
                        bestlen = cur_len;
                    }
                }
            }
            // 分配区间[chose_l, chose_r]
            // 移除原空闲段，插入剩下的左右（如有）
            auto it = freeSeg.lower_bound({chose_l, -1});
            auto actual = it;
            if(it == freeSeg.end() || it->first != chose_l)
                actual = prev(it);
            long long old_l = actual->first, old_r = actual->second;
            freeSeg.erase(actual);
            if(old_l < chose_l)
                freeSeg.insert({old_l, chose_l-1});//这两行没啥用
            if(chose_r < old_r)
                freeSeg.insert({chose_r+1, old_r});
            proc[p].push_back(Interface(chose_l, chose_r));
            cout << chose_l << '\n';
        }
        else if(cmd == "send") {
            int p;
            cin >> p;
            long long sum = 0;
            for(auto &iface : proc[p]) {
                int len = iface.r - iface.l + 1;
                long long addr = iface.l + iface.head;
                sum += addr;
                iface.head = (iface.head + 1) % len;
            }
            cout << sum << '\n';
        }
        else if(cmd == "delete") {
            int p, idx;
            cin >> p >> idx;
            --idx; // 题目接口从1开始，vector下标0开始
            Interface sel = proc[p][idx];
            // 归还内存段[l, r]，合并相邻区间
            long long l = sel.l, r = sel.r;
            // 找能合并的左右
            auto it = freeSeg.lower_bound({l, -1});
            bool mergedL = false, mergedR = false;
            // 左边能合
            if(it != freeSeg.begin()) {
                auto prv = prev(it);
                if(prv->second + 1 == l) {
                    l = prv->first;
                    freeSeg.erase(prv);
                    mergedL = true;
                }
            }
            // 右边能合
            if(it != freeSeg.end() && it->first == r + 1) {
                r = it->second;
                freeSeg.erase(it);
                mergedR = true;
            }
            freeSeg.insert({l, r});
            // 标记删除接口
            proc[p].erase(proc[p].begin() + idx);
        }
    }
    return 0;
}
