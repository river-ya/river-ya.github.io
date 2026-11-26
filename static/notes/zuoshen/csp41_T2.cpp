#include <bits/stdc++.h>
using namespace std;
struct task{
    int type, t, a, b, idx;
    double eff() const {
        return double(b) / a;
    }
};
int main(){
    int n, m;
    cin >> n >> m;
    vector<task> flexible, fixed;
    int sum_t = 0;
    for (int i = 0;i<n;i++){
        int o, t, a, b;
        cin >> o >> t >> a >> b;
        sum_t += t;
        if (o == 0){
            flexible.push_back({o, t, a, b, i});
        }
        else{
            fixed.push_back({o, t, a, b, i});
        }
    }
    //dp[j] 普通型分配j杯咖啡能获得的最大总缩短
    vector<double> dp(m + 1, 0);
    for (auto & ele : fixed){
        int a = ele.a, b = ele.b;
        for (int j = m; j>=a; --j){
            dp[j] = max(dp[j], dp[j - a] + b);
        }
    }
    sort(flexible.begin(), flexible.end(), [](const task & x, const task & y){
        return x.eff() > y.eff();
    });
    double ans = 1e18;
    for (int used = 0; used <= m; used++){
        double flex_reduction = 0.0;
        int left = m - used;
        int remain = left;
        for (auto & ele : flexible){
            int give = min(remain, ele.a);
            double real_give = give;
            flex_reduction += ele.eff() * real_give;
            remain -= give;
            if (remain == 0) break;
        }
        double total = sum_t - dp[used] - flex_reduction;
        ans = min(ans, total);
    }
    printf("%.6f", ans);
    return 0;
}
