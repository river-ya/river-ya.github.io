[洛谷 P1242](https://www.luogu.com.cn/problem/P1242)

## 题目描述

设有 $n$ 个大小不等的中空圆盘，按从小到大的顺序从 $1$ 到 $n$ 编号。将这 $n$ 个圆盘任意的迭套在三根立柱上，立柱的编号分别为 $A,B,C$，这个状态称为初始状态。

现在要求找到一种步数最少的移动方案，使得从初始状态转变为目标状态。

移动时有如下要求：

- 一次只能移一个盘；
- 不允许把大盘移到小盘上面。

## 输入格式

第一行一个整数，表示圆盘总数 $n$。

接下来三行每行若干个整数，分别代表初始状态下 $A, B, C$ 柱子上的圆盘数量和从下到上的圆盘编号，如果只有一个数 $0$ 就代表这根柱子上没有圆盘。

接下来三行每行若干个整数，分别代表目标状态下 $A, B, C$ 柱子上的圆盘数量和从下到上的圆盘编号，如果只有一个数 $0$ 就代表这根柱子上没有圆盘。

## 输出格式

若干行每行一个字符串，格式为 `move I from P to Q`，代表一个移动的操作。其中 $I$ 是圆盘编号，$P$ 和 $Q$ 是立柱编号，表示将圆盘 $I$ 从立柱 $P$ 移到立柱 $Q$。

接下来一行一个整数，代表从初始状态到目标状态的最少步数。你可以假定步数不会超过 $32767$。如果有多种移动的方式，输出任意一种都算正确。

## 输入输出样例 #1

### 输入 #1

```
5
3 3 2 1
2 5 4
0
1 2
3 5 4 3
1 1
```

### 输出 #1

```
move 1 from A to B
move 2 from A to C
move 1 from B to C
move 3 from A to B
move 1 from C to B
move 2 from C to A
move 1 from B to C
7
```

## 说明/提示

#### 数据规模与约定

对于 $100\%$ 的数据，$1 \le n \le 45$，$1 \le $ 每个圆盘的编号 $\le n$。





递归处理

对于k号圆盘

如果pos[k] == target[k]，那么不用移动，此步已完成，递归完成前k-1个圆盘即可

如果pos[k] != target[k]，那么对于k号圆盘，前k-1个圆盘都必须移动到最后一根柱子上（区别于pos[k]和target[k]的柱子）

假设pos[k] = A, target[k] = B，于是可以分为三个步骤：

* 将前k-1个圆盘移动到C
* 将k号圆盘放至B
* 将前k-1个圆盘移动到各自的目标位置

第二步是一个简单的赋值操作，第三步是对于k号圆盘放到目标位置同样的操作

第三根柱子可以直接算

```cpp
int from = pos[k];
int to = target[k];
int other = 3 - from - to; // 0 + 1 + 2 = 3
```

接下来需要解决第一步，可以解释为

**如何将前k个圆盘移动到一根柱子上**

还是递归思想

假如不考虑最少步数，直接递归

```cpp
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
void solve(int k){
	if (k == 0) return;
	if (pos[k] == target[k]){
		solve(k - 1);
		return;
	}
	int other = 3 - pos[k] - target[k];
	move_gather(k - 1, other);
	move_one(k, target[k]);
	solve(k - 1);
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
```

![image-20261125205314682](/assets/notes/labs/p1242-judging.png)

WA了，看来还是需要考虑最少步数这一条件

假如最大圆盘需要从A移动到B，那么存在两种可能：
方案一，最大圆盘直接移动一次

方案二，最大圆盘经过中间柱子移动两次

虽然方案二多移动了一次圆盘，但可能减少很多小圆盘的移动次数，所以需要比较两种方案的总步数



定义 $F(k,p,S)$ 表示：

将状态 $S$ 中编号为 $1 \sim k$ 的圆盘全部移动到柱子$p$ 上所需要的最少步数。

其中：

- $k$：当前考虑的最大圆盘编号。
- $p$：希望将所有圆盘集中到的目标柱子。
- $S$：所有圆盘的初始位置状态。
- $S_k$：编号为 $k$ 的圆盘当前所在的柱子。
- $q$：不同于 $S_k$ 和 $p$ 的第三根柱子。

由于每根柱子上的圆盘一定按照从大到小的顺序排列，
因此只需要记录每个圆盘所在的柱子，就可以唯一确定整个状态。

递归公式如下：

$$
F(k,p,S)=
\begin{cases}
0 & k=0\\
F(k-1,p,S) & S_k=p\\
F(k-1,q,S)+2^{k-1} & S_k\neq p
\end{cases}
$$

下面分别讨论三种情况。

### 情况一：$k=0$

当前没有任何圆盘需要移动，因此移动步数为 0。

$$
F(0,p,S)=0
$$

这是递归的终止条件。

### 情况二：$S_k=p$

当前最大的圆盘 $k$ 已经位于目标柱子 $p$ 上。

由于圆盘 $k$ 比其余所有圆盘都大，所以它不会阻碍
前 $k-1$ 个圆盘的移动，也没有必要移动它。

因此，原问题可以直接转化为：

将前 $k-1$ 个圆盘全部移动到柱子 $p$。

$$
F(k,p,S)=F(k-1,p,S)
$$

### 情况三：$S_k\neq p$

假设圆盘 $k$ 当前位于柱子 A，目标柱子为 B，第三根柱子为 C。

由于汉诺塔不允许大盘压小盘，因此要移动圆盘 $k$，必须满足以下两个条件：

1. A 柱上不能有比圆盘 $k$ 更小的圆盘，否则无法取出圆盘 $k$。
2. B 柱上不能有比圆盘 $k$ 更小的圆盘，否则无法将圆盘 $k$ 放到 B 柱上。

因此，必须先将前 $k-1$ 个圆盘全部集中到第三根柱子 C。

整个移动过程可以划分为三个阶段。

#### 第一阶段：将前 $k-1$ 个圆盘集中到第三根柱子 $q$

由于前 $k-1$ 个圆盘最初可能任意分布在三根柱子上，
所以这是一个规模缩小后的新汉诺塔问题。

所需步数为：

$$
T_1=F(k-1,q,S)
$$

此时：

- 圆盘 $k$ 仍然位于 A 柱。
- 前 $k-1$ 个圆盘全部位于 C 柱。
- B 柱上没有比圆盘 $k$ 更小的圆盘。

#### 第二阶段：移动圆盘 $k$

直接将圆盘 $k$ 从 A 柱移动到目标柱子 B。

只需要移动一次，因此：

$$
T_2=1
$$

#### 第三阶段：将前 $k-1$ 个圆盘整体移动到目标柱子 $p$

此时，前 $k-1$ 个圆盘已经全部集中在 C 柱上，
需要将它们整体移动到 B 柱。

与第一阶段不同，此时所有待移动的圆盘已经集中在
同一根柱子上，因此问题退化为传统汉诺塔问题。

传统汉诺塔将 $m$ 个圆盘从一根柱子整体移动到
另一根柱子所需的最少步数为：

$$
H(m)=2^m-1
$$

令 $m=k-1$，得到：

$$
T_3=H(k-1)=2^{k-1}-1
$$

#### 合并三个阶段

将三个阶段的步数相加：

$$
\begin{aligned}
F(k,p,S)
&=T_1+T_2+T_3\\
&=F(k-1,q,S)+1+(2^{k-1}-1)\\
&=F(k-1,q,S)+2^{k-1}
\end{aligned}
$$

因此：

$$
\boxed{F(k,p,S)=F(k-1,q,S)+2^{k-1}}
$$

## 传统汉诺塔的步数？

设 $H(m)$ 表示将集中在一根柱子上的 $m$ 个圆盘
全部移动到另一根柱子的最少步数。

其过程同样可以划分为三个阶段：

1. 将前 $m-1$ 个圆盘移动到辅助柱：$H(m-1)$ 步。
2. 将最大的圆盘移动到目标柱：$1$ 步。
3. 将前 $m-1$ 个圆盘移动到目标柱：$H(m-1)$ 步。

因此：

$$
H(m)=2H(m-1)+1
$$

递归展开：

$$
\begin{aligned}
H(m)
&=2H(m-1)+1\\
&=2^2H(m-2)+2+1\\
&=2^3H(m-3)+2^2+2+1\\
&\quad\vdots\\
&=2^mH(0)+\sum_{i=0}^{m-1}2^i
\end{aligned}
$$

由于 $H(0)=0$，根据等比数列求和公式：



### 第五阶段：将前 $k-1$ 个圆盘分散到目标位置

此时所有的小圆盘都集中在 A 柱上。

但是最终目标状态 target 中，这些圆盘可能分布在任意柱子上。

因此，需要计算从 A 柱的集中状态出发，到达目标状态 $T$ 的最少步数。

然而，已经定义的函数 $F(k,p,S)$ 只能计算从任意状态到集中状态的最少步数。

这里可以利用汉诺塔移动的可逆性。对于任意两个合法状态 $X$ 和 $Y$，从 $X$到 $Y$ 的每一个合法移动都可以反向执行。

因此有：

$$
\operatorname{dist}(X,Y)
=
\operatorname{dist}(Y,X)
$$

令 $P_a$ 表示所有小圆盘集中在 A 柱上的状态，
则有：

$$
\begin{aligned}
T_5
&=\operatorname{dist}(P_a,T)\\
&=\operatorname{dist}(T,P_a)\\
&=F(k-1,a,T)
\end{aligned}
$$

对应代码：

```cpp
+ cost(k - 1, a, target)
```

```cpp
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
```

<a href="/assets/source/p1242.cpp" download>下载 C++ 源码</a>
