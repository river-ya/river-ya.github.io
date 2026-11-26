[洛谷 P1242](https://www.luogu.com.cn/problem/P1242)

## 题目描述

设有 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>n</mi></mrow></math> 个大小不等的中空圆盘，按从小到大的顺序从 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn></mrow></math> 到 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>n</mi></mrow></math> 编号。将这 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>n</mi></mrow></math> 个圆盘任意的迭套在三根立柱上，立柱的编号分别为 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>A</mi><mo>&#x0002C;</mo><mi>B</mi><mo>&#x0002C;</mo><mi>C</mi></mrow></math>，这个状态称为初始状态。

现在要求找到一种步数最少的移动方案，使得从初始状态转变为目标状态。

移动时有如下要求：

- 一次只能移一个盘；
- 不允许把大盘移到小盘上面。

## 输入格式

第一行一个整数，表示圆盘总数 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>n</mi></mrow></math>。

接下来三行每行若干个整数，分别代表初始状态下 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>A</mi><mo>&#x0002C;</mo><mi>B</mi><mo>&#x0002C;</mo><mi>C</mi></mrow></math> 柱子上的圆盘数量和从下到上的圆盘编号，如果只有一个数 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>0</mn></mrow></math> 就代表这根柱子上没有圆盘。

接下来三行每行若干个整数，分别代表目标状态下 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>A</mi><mo>&#x0002C;</mo><mi>B</mi><mo>&#x0002C;</mo><mi>C</mi></mrow></math> 柱子上的圆盘数量和从下到上的圆盘编号，如果只有一个数 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>0</mn></mrow></math> 就代表这根柱子上没有圆盘。

## 输出格式

若干行每行一个字符串，格式为 `move I from P to Q`，代表一个移动的操作。其中 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>I</mi></mrow></math> 是圆盘编号，<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>P</mi></mrow></math> 和 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Q</mi></mrow></math> 是立柱编号，表示将圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>I</mi></mrow></math> 从立柱 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>P</mi></mrow></math> 移到立柱 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Q</mi></mrow></math>。

接下来一行一个整数，代表从初始状态到目标状态的最少步数。你可以假定步数不会超过 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>32767</mn></mrow></math>。如果有多种移动的方式，输出任意一种都算正确。

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

对于 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>100</mn><mi>&#x00025;</mi></mrow></math> 的数据，<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn><mo>&#x02264;</mo><mi>n</mi><mo>&#x02264;</mo><mn>45</mn></mrow></math>，<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn><mo>&#x02264;</mo></mrow></math> 每个圆盘的编号 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mo>&#x02264;</mo><mi>n</mi></mrow></math>。





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



定义 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo></mrow></math> 表示：

将状态 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>S</mi></mrow></math> 中编号为 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn><mi>&#x0007E;</mi><mi>k</mi></mrow></math> 的圆盘全部移动到柱子<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi></mrow></math> 上所需要的最少步数。

其中：

- <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math>：当前考虑的最大圆盘编号。
- <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi></mrow></math>：希望将所有圆盘集中到的目标柱子。
- <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>S</mi></mrow></math>：所有圆盘的初始位置状态。
- <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>S</mi><mi>k</mi></msub></mrow></math>：编号为 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 的圆盘当前所在的柱子。
- <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>q</mi></mrow></math>：不同于 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>S</mi><mi>k</mi></msub></mrow></math> 和 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi></mrow></math> 的第三根柱子。

由于每根柱子上的圆盘一定按照从大到小的顺序排列，
因此只需要记录每个圆盘所在的柱子，就可以唯一确定整个状态。

递归公式如下：
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mrow><mo stretchy="true" fence="true" form="prefix">&#x0007B;</mo><mtable><mtr><mtd columnalign="left"><mn>0</mn></mtd><mtd columnalign="left"><mi>k</mi><mo>&#x0003D;</mo><mn>0</mn></mtd></mtr><mtr><mtd columnalign="left"><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo></mtd><mtd columnalign="left"><msub><mi>S</mi><mi>k</mi></msub><mo>&#x0003D;</mo><mi>p</mi></mtd></mtr><mtr><mtd columnalign="left"><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>q</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><msup><mn>2</mn><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msup></mtd><mtd columnalign="left"><msub><mi>S</mi><mi>k</mi></msub><mo>&#x02260;</mo><mi>p</mi></mtd></mtr></mtable></mrow></mrow></math>

下面分别讨论三种情况。

### 情况一：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x0003D;</mo><mn>0</mn></mrow></math>

当前没有任何圆盘需要移动，因此移动步数为 0。

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mn>0</mn><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mn>0</mn></mrow></math>

这是递归的终止条件。

### 情况二：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>S</mi><mi>k</mi></msub><mo>&#x0003D;</mo><mi>p</mi></mrow></math>

当前最大的圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 已经位于目标柱子 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi></mrow></math> 上。

由于圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 比其余所有圆盘都大，所以它不会阻碍
前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘的移动，也没有必要移动它。

因此，原问题可以直接转化为：

将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘全部移动到柱子 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi></mrow></math>。

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo></mrow></math>

### 情况三：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>S</mi><mi>k</mi></msub><mo>&#x02260;</mo><mi>p</mi></mrow></math>

假设圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 当前位于柱子 A，目标柱子为 B，第三根柱子为 C。

由于汉诺塔不允许大盘压小盘，因此要移动圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math>，必须满足以下两个条件：

1. A 柱上不能有比圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 更小的圆盘，否则无法取出圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math>。
2. B 柱上不能有比圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 更小的圆盘，否则无法将圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 放到 B 柱上。

因此，必须先将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘全部集中到第三根柱子 C。

整个移动过程可以划分为三个阶段。

#### 第一阶段：将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘集中到第三根柱子 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>q</mi></mrow></math>

由于前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘最初可能任意分布在三根柱子上，
所以这是一个规模缩小后的新汉诺塔问题。

所需步数为：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mi>T</mi><mn>1</mn></msub><mo>&#x0003D;</mo><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>q</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo></mrow></math>

此时：

- 圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 仍然位于 A 柱。
- 前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘全部位于 C 柱。
- B 柱上没有比圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 更小的圆盘。

#### 第二阶段：移动圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math>

直接将圆盘 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi></mrow></math> 从 A 柱移动到目标柱子 B。

只需要移动一次，因此：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mi>T</mi><mn>2</mn></msub><mo>&#x0003D;</mo><mn>1</mn></mrow></math>

#### 第三阶段：将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘整体移动到目标柱子 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi></mrow></math>

此时，前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘已经全部集中在 C 柱上，
需要将它们整体移动到 B 柱。

与第一阶段不同，此时所有待移动的圆盘已经集中在
同一根柱子上，因此问题退化为传统汉诺塔问题。

传统汉诺塔将 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>m</mi></mrow></math> 个圆盘从一根柱子整体移动到
另一根柱子所需的最少步数为：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><msup><mn>2</mn><mi>m</mi></msup><mo>&#x02212;</mo><mn>1</mn></mrow></math>

令 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>m</mi><mo>&#x0003D;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math>，得到：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mi>T</mi><mn>3</mn></msub><mo>&#x0003D;</mo><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><msup><mn>2</mn><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msup><mo>&#x02212;</mo><mn>1</mn></mrow></math>

#### 合并三个阶段

将三个阶段的步数相加：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mi>&</mi><mo>&#x0003D;</mo><msub><mi>T</mi><mn>1</mn></msub><mo>&#x0002B;</mo><msub><mi>T</mi><mn>2</mn></msub><mo>&#x0002B;</mo><msub><mi>T</mi><mn>3</mn></msub><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>q</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><mn>1</mn><mo>&#x0002B;</mo><mo stretchy="false">&#x00028;</mo><msup><mn>2</mn><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msup><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>q</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><msup><mn>2</mn><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msup></mrow></mrow></math>

因此：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><menclose notation="box"><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>q</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><msup><mn>2</mn><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msup></mrow></menclose></mrow></math>

## 传统汉诺塔的步数？

设 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo stretchy="false">&#x00029;</mo></mrow></math> 表示将集中在一根柱子上的 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>m</mi></mrow></math> 个圆盘
全部移动到另一根柱子的最少步数。

其过程同样可以划分为三个阶段：

1. 将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>m</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘移动到辅助柱：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo></mrow></math> 步。
2. 将最大的圆盘移动到目标柱：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn></mrow></math> 步。
3. 将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>m</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘移动到目标柱：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo></mrow></math> 步。

因此：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mn>2</mn><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><mn>1</mn></mrow></math>

递归展开：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo stretchy="false">&#x00029;</mo><mi>&</mi><mo>&#x0003D;</mo><mn>2</mn><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><mn>1</mn><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><msup><mn>2</mn><mn>2</mn></msup><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo>&#x02212;</mo><mn>2</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><mn>2</mn><mo>&#x0002B;</mo><mn>1</mn><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><msup><mn>2</mn><mn>3</mn></msup><mi>H</mi><mo stretchy="false">&#x00028;</mo><mi>m</mi><mo>&#x02212;</mo><mn>3</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><msup><mn>2</mn><mn>2</mn></msup><mo>&#x0002B;</mo><mn>2</mn><mo>&#x0002B;</mo><mn>1</mn><mspace linebreak="newline" /><mi>&</mi><mspace width="1em" /><mo>&#x022EE;</mo><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><msup><mn>2</mn><mi>m</mi></msup><mi>H</mi><mo stretchy="false">&#x00028;</mo><mn>0</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><munderover><mo>&#x02211;</mo><mrow><mi>i</mi><mo>&#x0003D;</mo><mn>0</mn></mrow><mrow><mi>m</mi><mo>&#x02212;</mo><mn>1</mn></mrow></munderover><msup><mn>2</mn><mi>i</mi></msup></mrow></mrow></math>

由于 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>H</mi><mo stretchy="false">&#x00028;</mo><mn>0</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mn>0</mn></mrow></math>，根据等比数列求和公式：



### 第五阶段：将前 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></math> 个圆盘分散到目标位置

此时所有的小圆盘都集中在 A 柱上。

但是最终目标状态 target 中，这些圆盘可能分布在任意柱子上。

因此，需要计算从 A 柱的集中状态出发，到达目标状态 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>T</mi></mrow></math> 的最少步数。

然而，已经定义的函数 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x0002C;</mo><mi>p</mi><mo>&#x0002C;</mo><mi>S</mi><mo stretchy="false">&#x00029;</mo></mrow></math> 只能计算从任意状态到集中状态的最少步数。

这里可以利用汉诺塔移动的可逆性。对于任意两个合法状态 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>X</mi></mrow></math> 和 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Y</mi></mrow></math>，从 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>X</mi></mrow></math>到 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Y</mi></mrow></math> 的每一个合法移动都可以反向执行。

因此有：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mo>dist</mo><mo stretchy="false">&#x00028;</mo><mi>X</mi><mo>&#x0002C;</mo><mi>Y</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mo>dist</mo><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0002C;</mo><mi>X</mi><mo stretchy="false">&#x00029;</mo></mrow></math>

令 <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>P</mi><mi>a</mi></msub></mrow></math> 表示所有小圆盘集中在 A 柱上的状态，
则有：

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mrow><msub><mi>T</mi><mn>5</mn></msub><mi>&</mi><mo>&#x0003D;</mo><mo>dist</mo><mo stretchy="false">&#x00028;</mo><msub><mi>P</mi><mi>a</mi></msub><mo>&#x0002C;</mo><mi>T</mi><mo stretchy="false">&#x00029;</mo><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><mo>dist</mo><mo stretchy="false">&#x00028;</mo><mi>T</mi><mo>&#x0002C;</mo><msub><mi>P</mi><mi>a</mi></msub><mo stretchy="false">&#x00029;</mo><mspace linebreak="newline" /><mi>&</mi><mo>&#x0003D;</mo><mi>F</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02212;</mo><mn>1</mn><mo>&#x0002C;</mo><mi>a</mi><mo>&#x0002C;</mo><mi>T</mi><mo stretchy="false">&#x00029;</mo></mrow></mrow></math>

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
