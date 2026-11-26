#include <bits/stdc++.h>
using namespace std;
int n;
long long cnt = 0;
int pos[46], target[46];
void move_one(int k, int position){
	if(k == 0) return;
	char from = pos[k] + 'A';
	char to = position + 'A';
	printf("move %d from %c to %c\n", k, from, to);
	pos[k] = position;
	cnt++;
}
void move_gather(int k, int position){
	if (k == 0){
		return;
	}
	if (pos[k] == position){
		move_gather(k - 1, position);
	}
	else{
		int other = 3 - pos[k] - position;
		move_gather(k - 1, other);
		move_one(k, position);
		move_gather(k - 1, position);
	}
}
long long cost(int k, int position, const int s[]){
    if (k == 0) return 0;
    if (s[k] == position)
        return cost(k - 1, position, s);
    int other = 3 - s[k] - position;
    return cost(k - 1, other, s) + (1LL << (k - 1));
}
void solve(int k){
	if (k == 0) return;
	if (pos[k] == target[k]){
		solve(k - 1);
		return;
	}
	int a = pos[k];
	int b = target[k];
	int c = 3 - a - b;
	// 方案一：最大圆盘直接移动A -> B
	long long cost1 = cost(k - 1, c, pos) + 1 + cost(k - 1, c, target);
	// 方案二：最大圆盘移动两次，A -> C -> B
	long long cost2 = cost(k - 1, b, pos) + 1 + ((1LL << (k - 1)) - 1) + 1 + cost(k - 1, a, target);
	if (cost1 <= cost2){
		move_gather(k - 1, c);
		move_one(k, b);
		solve(k - 1);
	}
	else{
		move_gather(k - 1, b);
		move_one(k, c);
		move_gather(k - 1, a);
		move_one(k, b);
		solve(k - 1);
	}

}
int main(){
	cin >> n;
	// 直接根据编号存位于哪个柱子上，因为所有盘的相对位置已经确定
	for(int i = 0; i < 3; i++){
		int sz, x;
		cin >> sz;
		while(sz--){
			cin >> x;
			pos[x] = i;
		}
	}
	for (int i = 0; i < 3; i++){
		int sz, x;
		cin >> sz;
		while(sz--){
			cin >> x;
			target[x] = i;
		}
	}
	solve(n);
	printf("%lld\n", cnt);
	return 0;
}
