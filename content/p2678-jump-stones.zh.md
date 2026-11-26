[洛谷 P2678](https://www.luogu.com.cn/problem/P2678)

## 题目背景

NOIP2015 Day2T1

## 题目描述

一年一度的“跳石头”比赛又要开始了！

这项比赛将在一条笔直的河道中进行，河道中分布着一些巨大岩石。组委会已经选择好了两块岩石作为比赛起点和终点。在起点和终点之间，有 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>N</mi></mrow></math> 块岩石（不含起点和终点的岩石）。在比赛过程中，选手们将从起点出发，每一步跳向相邻的岩石，直至到达终点。

为了提高比赛难度，组委会计划移走一些岩石，使得选手们在比赛过程中的最短跳跃距离尽可能长。由于预算限制，组委会至多从起点和终点之间移走 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>M</mi></mrow></math> 块岩石（不能移走起点和终点的岩石）。

## 输入格式

第一行包含三个整数 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>L</mi><mo>&#x0002C;</mo><mi>N</mi><mo>&#x0002C;</mo><mi>M</mi></mrow></math>，分别表示起点到终点的距离，起点和终点之间的岩石数，以及组委会至多移走的岩石数。保证 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>L</mi><mo>&#x02265;</mo><mn>1</mn></mrow></math> 且 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>N</mi><mo>&#x02265;</mo><mi>M</mi><mo>&#x02265;</mo><mn>0</mn></mrow></math>。

接下来 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>N</mi></mrow></math> 行，每行一个整数，第 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>i</mi></mrow></math> 行的整数 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>D</mi><mi>i</mi></msub><mspace width="0.167em" /><mo stretchy="false">&#x00028;</mo><mn>0</mn><mo>&#x0003C;</mo><msub><mi>D</mi><mi>i</mi></msub><mo>&#x0003C;</mo><mi>L</mi><mo stretchy="false">&#x00029;</mo></mrow></math>， 表示第 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>i</mi></mrow></math> 块岩石与起点的距离。这些岩石按与起点距离从小到大的顺序给出，且不会有两个岩石出现在同一个位置。

## 输出格式

一个整数，即最短跳跃距离的最大值。

## 输入输出样例 #1

### 输入 #1

```
25 5 2
2
11
14
17
21
```

### 输出 #1

```
4
```

## 说明/提示

### 输入输出样例 1 说明

将与起点距离为 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>2</mn></mrow></math> 和 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>14</mn></mrow></math> 的两个岩石移走后，最短的跳跃距离为 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>4</mn></mrow></math>（从与起点距离 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>17</mn></mrow></math> 的岩石跳到距离 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>21</mn></mrow></math> 的岩石，或者从距离 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>21</mn></mrow></math> 的岩石跳到终点）。

### 数据规模与约定

对于 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>20</mn><mi>&#x00025;</mi></mrow></math>的数据，<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>0</mn><mo>&#x02264;</mo><mi>M</mi><mo>&#x02264;</mo><mi>N</mi><mo>&#x02264;</mo><mn>10</mn></mrow></math>。
对于 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>50</mn><mi>&#x00025;</mi></mrow></math> 的数据，<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>0</mn><mo>&#x02264;</mo><mi>M</mi><mo>&#x02264;</mo><mi>N</mi><mo>&#x02264;</mo><mn>100</mn></mrow></math>。
对于 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>100</mn><mi>&#x00025;</mi></mrow></math> 的数据，$0 \le M \le N \le 50000,1 \le L
 \le 10^9$。

##  解答

### 题目分析

本题是二分答案的经典题目，识别二分答案的方法之前已经总结过（见之前的笔记总结）：

二分答案法：（有点**逆向思维**的感觉，即验证答案是否正确）

* 估计**最终答案可能的范围**是什么,可以很粗略（说白了就是l和r的初始取值）
* 分析**问题的答案和给定条件的单调性**，大部分只用到**自然智慧**（大胆猜，如果没有单调性果断放弃二分答案）
* 建立一个**check函数**，当答案固定的情况下，判断给定的条件是否达标（check函数复杂度尽可能的低，**最坏O(n)**）
* 达标后记录答案去某侧二分，不断不断的二分，最终找到答案

本题的单调性在于：如果某个ans已经满足题意，即最短跳跃距离的最大值是ans，那么比ans更小的值一定满足题意，所以是向右侧二分

难点在于如何写check函数

这里有个小细节，D[n] = L，这个是为了考虑最后一个岩石到终点的距离，方便统一处理

check函数的意义是**能否通过移除不超过m块岩石，使所有跳跃距离都大于等于mid**

这里就采用last去保存上一块被保留的岩石与起点的距离，方便实时统计每次去掉/保留岩石的情况

### 源代码

```cpp
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
```

<a href="/assets/source/p2678.cpp" download>下载 C++ 源码</a>
