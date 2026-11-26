#include <bits/stdc++.h>
using namespace std;

bool check(int mid, vector<int> & d, int m, int n){
	// 能否通过移除不超过m块岩石，使所有跳跃距离都大于等于mid
	int last = 0; // 上一块被保留的岩石与起点的距离
	int cnt = 0;
	for (int i = 0; i <= n; i++){
		if (d[i] - last < mid){
			cnt++;
		}
		else{
			last = d[i];
		}
	}
	return cnt <= m;
}

int main(){
	// 要让最短跳跃距离尽可能长
	// 输出最短跳跃距离的最大值
	// 二分答案?
	// left = 0, right = L
	// 单调性：如果当前ans满足条件，那么比ans小的数一定也满足，往右二分
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int L, N, M;
	cin >> L >> N >> M;
	vector<int> D(N + 1);
	for (int i = 0; i < N; i++){
		cin >> D[i];
	}
	D[N] = L;
	int l = 0, r = L, mid = 0, ans = -1;
	while (l <= r){
		mid = l + (r - l) / 2;
		if (check(mid, D, M, N)){
			ans = mid;
			l = mid + 1;
		}
		else{
			r = mid - 1;
		}
	}
	cout << ans;
	return 0;
}
