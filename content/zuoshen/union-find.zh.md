# 并查集

![f8001736e95d635bf1d208cbbd5b2712_720](/assets/notes/zuoshen/union-find-01.jpg)

经典并查集两处优化

1.扁平化（调用findSet和isSameSet方法时就可以进行）

2.小挂大

并查集使用场景

1. 一开始每个元素都拥有自己的集合，在自己的集合里只有这个元素自己
2. int findSet(i) 查找i所在集合的代表元素，代表元素来代表元素i所在的集合
3. bool isSameSet(a, b) 判断a和b在不在一个集合里
4. void unionSet(a, b) a所在集合所有元素和b所在集合所有元素合并成一个集合
5. 各种操作单词调用的时间复杂度为O(1)(反阿克曼函数)

```cpp
const int maxn = 100001;
int father[maxn];
int setsize[maxn];
int stk[maxn];
void initSet(int n){
	for (int i = 0; i < n; i++){
		father[i] = i;
		setsize[i] = 1;
	}
}
int findSet(int x){
	//沿途收集了几个点
	int stksize = 0;
	while(father[x] != x){
		stk[stksize++] = x;
		x = father[x];
	}
	//沿途结点收集好了，x已经跳到了代表结点
	while (stksize > 0){
		father[stk[--stksize]] = x;
	}
	return x;
}
bool isSameSet(int x, int y){
	return findSet(x) == findSet(y);
}
void unionSet(int x, int y){
	int fx = findSet(x);
	int fy = findSet(y);
	//不在同一个集合里
	if (fx != fy){
		if(setsize[fx] >= setsize[fy]){
			father[fy] = fx;
			setsize[fx] += setsize[fy];
		}
		else{
			father[fx] = fy;
			setsize[fy] += setsize[fx];
		}
	}
}
```

## [luogu P3367 并查集](https://www.luogu.com.cn/problem/P3367#ide)

```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn = 200005;
int father[maxn];
int setsize[maxn];
int stk[maxn];
void initSet(int n){
	for(int i = 0; i<=n;i++){//注意下标开始往往是1
		father[i] = i;
		setsize[i] = 1;
	}
}
int findSet(int x){
	int stksize = 0;
	while (x != father[x]){
		stk[stksize++] = x;
		x = father[x];
	}
	while (stksize>0){
		father[stk[--stksize]] = x;
	}
	return x;
}
int isSameSet(int a, int b){
	return findSet(a) == findSet(b);
}
void unionSet(int a, int b){
	int fa = findSet(a);
	int fb = findSet(b);//不是直接father，需要找代表元素
	if (fa != fb){
		if (setsize[fa] >= setsize[fb]){
			father[fb] = fa;
			setsize[fa] += setsize[fb];
		}
		else{
			father[fa] = fb;
			setsize[fb] += setsize[fa];
		}
	}
}
int main(){
	int n, m;
	cin >> n >> m;
	initSet(n);
	while (m--){
		int op, x, y;
		cin >> op >> x >> y;
		if(op == 1){
			unionSet(x, y);
		}
		else{
			cout << (isSameSet(x, y) ? "Y" : "N") << "\n";
		}
	}
	return 0;
}
```

## [leetcode No.765 情侣牵手](https://leetcode.cn/problems/couples-holding-hands/description/)

`n` 对情侣坐在连续排列的 `2n` 个座位上，想要牵到对方的手。

人和座位由一个整数数组 `row` 表示，其中 `row[i]` 是坐在第 `i `个座位上的人的 **ID**。情侣们按顺序编号，第一对是 `(0, 1)`，第二对是 `(2, 3)`，以此类推，最后一对是 `(2n - 2, 2n - 1)`。

返回 *最少交换座位的次数，以便每对情侣可以并肩坐在一起*。 *每次*交换可选择任意两人，让他们站起来交换座位。



**示例 1:**

```
输入: row = [0,2,1,3]
输出: 1
解释: 只需要交换第二个人（row[1]）和第三个人（row[2]）的位置即可。
```

**示例 2:**

```
输入: row = [3,2,0,1]
输出: 0
解释: 无需交换座位，所有的情侣都已经可以手牵手了。
```



**提示:**

- `2n == row.length`
- `2 <= n <= 30`
- `n` 是偶数
- `0 <= row[i] < 2n`
- `row` 中所有元素均 **无重复**

![a42784557a4ec92d899d37cd8882b12d](/assets/notes/zuoshen/union-find-02.jpg)

![2895ca91d39fe336c7c687fb76993f7f](/assets/notes/zuoshen/union-find-03.jpg)

k对混乱的情侣经过k-1次操作一定能配好（每操作一次都可以让一对情侣组好，最后两对情侣只需操作一次）

```cpp
const int maxn = 32;
int m = 0;
class Solution {
public:
    int father[maxn];
    int stk[maxn];
    int setsize[maxn];
    void initSet(int n){
        for (int i = 0; i<n;i++){
            father[i] = i;
            setsize[i] = 1;
        }
        m = n;//初始时总共有多少个不同的集合
    }
    int findSet(int x){
        int stksize = 0;
        while (x != father[x]){
            stk[stksize++] = x;
            x = father[x];
        }
        while (stksize > 0){
            father[stk[--stksize]] = x;
        }
        return x;
    }
    bool isSameSet(int a, int b){
        return findSet(a) == findSet(b);
    }
    void unionSet(int a, int b){
        int fa = findSet(a);
        int fb = findSet(b);
        if (fa != fb){
            if (setsize[fa] >= setsize[fb]){
                father[fb] = fa;
                setsize[fa] += setsize[fb];

            }
            else{
                father[fa] = fb;
                setsize[fb] += setsize[fa];
            }
            m--;//每次合并成功就减少一个集合
        }
    }

    int minSwapsCouples(vector<int>& row) {
        int n = row.size() / 2;
        initSet(n);
        for (int i = 0; i < n;i++){
            unionSet(row[2 * i]/2, row[2 * i + 1]/2);
        }
        return n - m;
    }
};
```

## [leetcode No.839 相似字符串组](https://leetcode.cn/problems/similar-string-groups/description/)

如果交换字符串 `X` 中的两个不同位置的字母，使得它和字符串 `Y` 相等，那么称 `X` 和 `Y` 两个字符串相似。如果这两个字符串本身是相等的，那它们也是相似的。

例如，`"tars"` 和 `"rats"` 是相似的 (交换 `0` 与 `2` 的位置)； `"rats"` 和 `"arts"` 也是相似的，但是 `"star"` 不与 `"tars"`，`"rats"`，或 `"arts"` 相似。

总之，它们通过相似性形成了两个关联组：`{"tars", "rats", "arts"}` 和 `{"star"}`。注意，`"tars"` 和 `"arts"` 是在同一组中，即使它们并不相似。形式上，对每个组而言，要确定一个单词在组中，只需要这个词和该组中至少一个单词相似。

给你一个字符串列表 `strs`。列表中的每个字符串都是 `strs` 中其它所有字符串的一个字母异位词。请问 `strs` 中有多少个相似字符串组？



**示例 1：**

```
输入：strs = ["tars","rats","arts","star"]
输出：2
```

**示例 2：**

```
输入：strs = ["omv","ovm"]
输出：1
```



**提示：**

- `1 <= strs.length <= 300`
- `1 <= strs[i].length <= 300`
- `strs[i]` 只包含小写字母。
- `strs` 中的所有单词都具有相同的长度，且是彼此的字母异位词。

```cpp
//时间复杂度：O(n)
const int maxn = 301;
int counts;
class Solution {
public:
    int father[maxn];
    int setsize[maxn];
    int stk[maxn];
    void initSet(int n){
        for (int i = 0; i<n;i++){
            father[i] = i;
            setsize[i] = 1;
        }
        counts = n;
    }
    int findSet(int x){
        int stksize = 0;
        while (x != father[x]){
            stk[stksize++] = x;
            x = father[x];
        }
        while (stksize>0){
            father[stk[--stksize]] = x;
        }
        return x;
    }
    void unionSet(int a, int b){
        int fa = findSet(a);
        int fb = findSet(b);
        if (fa != fb){
            if (setsize[fa] >= setsize[fb]){
                father[fb] = fa;
                setsize[fa] += setsize[fb];
            }
            else{
                father[fa] = fb;
                setsize[fb] += setsize[fa];
            }
            counts--;
        }
    }
    int numSimilarGroups(vector<string>& strs) {
        int n = strs.size();
        initSet(n);
        for (int i = 0;i<n;i++){
            for (int j = i + 1;j<n;j++){
                int diff = 0;
                int k = 0;
                if (findSet(i) != findSet(j)){
                    while (k < strs[0].size() && diff < 3){
                        if (strs[i][k] != strs[j][k]){
                            diff++;
                        }
                        k++;
                    }
                    if (diff == 0 || diff == 2){
                        unionSet(i, j);
                    }
                }
            }
        }
        return counts;
    }
};
```

## [leetcode No.200 岛屿数量](https://leetcode.cn/problems/number-of-islands/)

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。



**示例 1：**

```
输入：grid = [
  ['1','1','1','1','0'],
  ['1','1','0','1','0'],
  ['1','1','0','0','0'],
  ['0','0','0','0','0']
]
输出：1
```

**示例 2：**

```
输入：grid = [
  ['1','1','0','0','0'],
  ['1','1','0','0','0'],
  ['0','0','1','0','0'],
  ['0','0','0','1','1']
]
输出：3
```



**提示：**

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` 的值为 `'0'` 或 `'1'`

```cpp
const int maxn = 100000;
int counts = 0;
class Solution {
public:
    int father[maxn];
    int setsize[maxn];
    int stk[maxn];
    void initSet(int n, vector<int> & nums){
        counts = 0;
        for (int i = 0;i<n;i++){
            if (nums[i] == 1){
                father[i] = i;
                setsize[i] = 1;
                counts++;
            }
        }
    }
    int findSet(int x){
        int stksize = 0;
        while (x != father[x]){
            stk[stksize++] = x;
            x = father[x];
        }
        while(stksize > 0){
            father[stk[--stksize]] = x;
        }
        return x;
    }
    void unionSet(int a, int b){
        int fa = findSet(a);
        int fb = findSet(b);
        if (fa != fb){
            if (setsize[fa] >= setsize[fb]){
                father[fb] = fa;
                setsize[fa] += setsize[fb];
            }
            else{
                father[fa] = fb;
                setsize[fb] += setsize[fa];
            }
            counts--;
        }
    }
    int numIslands(vector<vector<char>>& grid) {
        int n = grid.size();
        int m = grid[0].size();
        vector<int> nums(n * m, 0);
        for (int i = 0;i<n;i++){
            for (int j = 0;j<m;j++){
                nums[m * i + j] = grid[i][j] - '0';
            }
        }
        initSet(n * m, nums);
        cout << counts << endl;
        for (int i = 0;i<n * m;i++){
            if (nums[i] == 1){
                if (i + m < n * m && nums[i + m] == 1){
                    unionSet(i, i + m);
                }
                if (i + 1 < n * m && (i + 1) % m != 0 && nums[i + 1] == 1){//小心跨行问题，要确保i+1和i在同一行才能算连通
                    unionSet(i + 1, i);
                }
            }

        }
        return counts;
    }
};
```

## [leetcode No.947 移除最多的同行或同列石头](https://leetcode.cn/problems/most-stones-removed-with-same-row-or-column/description/)

`n` 块石头放置在二维平面中的一些整数坐标点上。每个坐标点上最多只能有一块石头。

如果一块石头的 **同行或者同列** 上有其他石头存在，那么就可以移除这块石头。

给你一个长度为 `n` 的数组 `stones` ，其中 `stones[i] = [xi, yi]` 表示第 `i` 块石头的位置，返回 **可以移除的石子** 的最大数量。



**示例 1：**

```
输入：stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
输出：5
解释：一种移除 5 块石头的方法如下所示：
1. 移除石头 [2,2] ，因为它和 [2,1] 同行。
2. 移除石头 [2,1] ，因为它和 [0,1] 同列。
3. 移除石头 [1,2] ，因为它和 [1,0] 同行。
4. 移除石头 [1,0] ，因为它和 [0,0] 同列。
5. 移除石头 [0,1] ，因为它和 [0,0] 同行。
石头 [0,0] 不能移除，因为它没有与另一块石头同行/列。
```

**示例 2：**

```
输入：stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
输出：3
解释：一种移除 3 块石头的方法如下所示：
1. 移除石头 [2,2] ，因为它和 [2,0] 同行。
2. 移除石头 [2,0] ，因为它和 [0,0] 同列。
3. 移除石头 [0,2] ，因为它和 [0,0] 同行。
石头 [0,0] 和 [1,1] 不能移除，因为它们没有与另一块石头同行/列。
```

**示例 3：**

```
输入：stones = [[0,0]]
输出：0
解释：[0,0] 是平面上唯一一块石头，所以不可以移除它。
```



**提示：**

- `1 <= stones.length <= 1000`
- `0 <= xi, yi <= 104`
- 不会有两块石头放在同一个坐标点上

```cpp
const int maxn = 1001;
int counts;
class Solution {
public:
    int father[maxn];
    void initSet(int n){//每一个集合的下标是stones中的下标
        for (int i = 0;i<n;i++){
            father[i] = i;
        }
        counts = n;
    }
    int findSet(int x){
        if (father[x] != x){
            father[x] = findSet(father[x]);
        }
        return father[x];
    }
    void unionSet(int x, int y){
        int fx = findSet(x);
        int fy = findSet(y);
        if (fx != fy){
            father[fx] = fy;
            counts--;
        }
    }
    int removeStones(vector<vector<int>>& stones) {
        unordered_map<int, int> rowfirst, colfirst;//离散化处理用哈希表，但是要分成两个哈希表，因为只有key方便查询
        int n = stones.size();
        initSet(n);
        for (int i = 0; i<n;i++){
            if (!rowfirst.count(stones[i][0])){
                rowfirst[stones[i][0]] = i;
            }
            else{
                unionSet(rowfirst[stones[i][0]], i);
            }
            if (!colfirst.count(stones[i][1])){
                colfirst[stones[i][1]] = i;
            }
            else{
                unionSet(colfirst[stones[i][1]], i);
            }
        }
        return n - counts;
    }
};
```

## [leetcode No.2092 找出知晓所有秘密的所有专家](https://leetcode.cn/problems/find-all-people-with-secret/description/)

给你一个整数 `n` ，表示有 `n` 个专家从 `0` 到 `n - 1` 编号。另外给你一个下标从 0 开始的二维整数数组 `meetings` ，其中 `meetings[i] = [xi, yi, timei]` 表示专家 `xi` 和专家 `yi` 在时间 `timei` 要开一场会。一个专家可以同时参加 **多场会议** 。最后，给你一个整数 `firstPerson` 。

专家 `0` 有一个 **秘密** ，最初，他在时间 `0` 将这个秘密分享给了专家 `firstPerson` 。接着，这个秘密会在每次有知晓这个秘密的专家参加会议时进行传播。更正式的表达是，每次会议，如果专家 `xi` 在时间 `timei` 时知晓这个秘密，那么他将会与专家 `yi` 分享这个秘密，反之亦然。

秘密共享是 **瞬时发生** 的。也就是说，在同一时间，一个专家不光可以接收到秘密，还能在其他会议上与其他专家分享。

在所有会议都结束之后，返回所有知晓这个秘密的专家列表。你可以按 **任何顺序** 返回答案。



**示例 1：**

```
输入：n = 6, meetings = [[1,2,5],[2,3,8],[1,5,10]], firstPerson = 1
输出：[0,1,2,3,5]
解释：
时间 0 ，专家 0 将秘密与专家 1 共享。
时间 5 ，专家 1 将秘密与专家 2 共享。
时间 8 ，专家 2 将秘密与专家 3 共享。
时间 10 ，专家 1 将秘密与专家 5 共享。
因此，在所有会议结束后，专家 0、1、2、3 和 5 都将知晓这个秘密。
```

**示例 2：**

```
输入：n = 4, meetings = [[3,1,3],[1,2,2],[0,3,3]], firstPerson = 3
输出：[0,1,3]
解释：
时间 0 ，专家 0 将秘密与专家 3 共享。
时间 2 ，专家 1 与专家 2 都不知晓这个秘密。
时间 3 ，专家 3 将秘密与专家 0 和专家 1 共享。
因此，在所有会议结束后，专家 0、1 和 3 都将知晓这个秘密。
```

**示例 3：**

```
输入：n = 5, meetings = [[3,4,2],[1,2,1],[2,3,1]], firstPerson = 1
输出：[0,1,2,3,4]
解释：
时间 0 ，专家 0 将秘密与专家 1 共享。
时间 1 ，专家 1 将秘密与专家 2 共享，专家 2 将秘密与专家 3 共享。
注意，专家 2 可以在收到秘密的同一时间分享此秘密。
时间 2 ，专家 3 将秘密与专家 4 共享。
因此，在所有会议结束后，专家 0、1、2、3 和 4 都将知晓这个秘密。
```



**提示：**

- `2 <= n <= 105`

- `1 <= meetings.length <= 105`

- `meetings[i].length == 3`

- `0 <= xi, yi <= n - 1`

- `xi != yi`

- `1 <= timei <= 105`

- `1 <= firstPerson <= n - 1`

```cpp
// 1. 搞清楚代表元素需要什么标签，标签怎么更新
//本题中：代表元素的标签是该圈子是否知晓秘密，更新方法：如果两个人中至少有一个人的代表元素知晓秘密那么这两个人合并在一起后都将知晓秘密，只需要改代表元素为secret[fx] |= secret[fy]
// 2. 是多组合并还是多次合并，多组合并的话怎么划分组，而且需要考虑撤销的方法，一般变回init状态就行
//本题是多组合并，根据times来分组，依据times进行排序，然后左右指针扫描，每次处理时间相同的区间，撤销的方法：在做完整个小区间里的所有合并后，依次查看每个人的代表元素标签是不是true，不是则还原回father[i] = i;
const int maxn = 100001;
class Solution {
public:
    int father[maxn];
    int setsize[maxn];
    int stk[maxn];
    //集合的标签属性：设置集合的一些属性
    //secret[代表元素] 代表元素的属性
    bool secret[maxn] = {false};
    void initSet(int n){
        for (int i = 0;i<n;i++){
            father[i] = i;
            setsize[i] = 1;
        }
        secret[0] = true;
    }
    int findSet(int x){
        int stksize = 0;
        while (x != father[x]){
            stk[stksize++] = x;
            x = father[x];
        }
        while (stksize > 0){
            father[stk[--stksize]] = x;
        }
        return x;
    }
    void unionSet(int x, int y){
        int fx = findSet(x);
        int fy = findSet(y);
        if (fx != fy){
            if (setsize[fx] >= setsize[fy]){
                father[fy] = fx;
                secret[fx] |= secret[fy];
                setsize[fx] += setsize[fy];
            }
            else{
                father[fx] = fy;
                secret[fy] |= secret[fx];
                setsize[fy] = setsize[fx];
            }

        }
    }
    static bool cmp(vector<int> & a, vector<int> & b){
        return a[2] < b[2];
    }
    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        initSet(n);
        sort(meetings.begin(), meetings.end(), cmp);//关键排序,时间先后很重要，只考虑同一时刻的合并
        unionSet(0, firstPerson);
        int m = meetings.size();
        for (int l = 0, r; l < m;){
            r = l;
            while (r + 1 < m && meetings[r+1][2] == meetings[l][2]){
                r++;
            }
            //l …… r 一定是公共时刻
            for (int i = l; i <= r;i++){
                unionSet(meetings[i][0], meetings[i][1]);
            }
            //撤销不知晓秘密的圈子
            for (int i = l, a, b; i <= r;i++){
                a = meetings[i][0];
                b = meetings[i][1];
                if (!secret[findSet(a)]){
                    father[a] = a;
                }
                if (!secret[findSet(b)]){
                    father[b] = b;
                }
            }
            l = r + 1;
        }
        vector<int> ans;
        for (int i = 0;i<n;i++){
            if (secret[findSet(i)]){
                ans.push_back(i);
            }
        }
        return ans;
    }
};
```

## [leetcode No.2421 好路径的数目](https://leetcode.cn/problems/number-of-good-paths/description/)

给你一棵 `n` 个节点的树（连通无向无环的图），节点编号从 `0` 到 `n - 1` 且恰好有 `n - 1` 条边。

给你一个长度为 `n` 下标从 **0** 开始的整数数组 `vals` ，分别表示每个节点的值。同时给你一个二维整数数组 `edges` ，其中 `edges[i] = [ai, bi]` 表示节点 `ai` 和 `bi` 之间有一条 **无向** 边。

一条 **好路径** 需要满足以下条件：

1. 开始节点和结束节点的值 **相同** 。
2. 开始节点和结束节点中间的所有节点值都 **小于等于** 开始节点的值（也就是说开始节点的值应该是路径上所有节点的最大值）。

请你返回不同好路径的数目。

注意，一条路径和它反向的路径算作 **同一** 路径。比方说， `0 -> 1` 与 `1 -> 0` 视为同一条路径。单个节点也视为一条合法路径。



**示例 1：**

![img](https://assets.leetcode.com/uploads/2022/08/04/f9caaac15b383af9115c5586779dec5.png)

```
输入：vals = [1,3,2,1,3], edges = [[0,1],[0,2],[2,3],[2,4]]
输出：6
解释：总共有 5 条单个节点的好路径。
还有 1 条好路径：1 -> 0 -> 2 -> 4 。
（反方向的路径 4 -> 2 -> 0 -> 1 视为跟 1 -> 0 -> 2 -> 4 一样的路径）
注意 0 -> 2 -> 3 不是一条好路径，因为 vals[2] > vals[0] 。
```

**示例 2：**

![img](https://assets.leetcode.com/uploads/2022/08/04/149d3065ec165a71a1b9aec890776ff.png)

```
输入：vals = [1,1,2,2,3], edges = [[0,1],[1,2],[2,3],[2,4]]
输出：7
解释：总共有 5 条单个节点的好路径。
还有 2 条好路径：0 -> 1 和 2 -> 3 。
```

**示例 3：**

![img](https://assets.leetcode.com/uploads/2022/08/04/31705e22af3d9c0a557459bc7d1b62d.png)

```
输入：vals = [1], edges = []
输出：1
解释：这棵树只有一个节点，所以只有一条好路径。
```



**提示：**

- `n == vals.length`
- `1 <= n <= 3 * 104`
- `0 <= vals[i] <= 105`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= ai, bi < n`
- `ai != bi`
- `edges` 表示一棵合法的树。

![bf823be3b01472d392a1b3e3fd99e24c_720](/assets/notes/zuoshen/union-find-04.jpg)



```cpp
//代表元素的标签：最大值，最大值的个数
//             maxval[maxn], maxcnt[maxn]
//这道题分不分组无所谓，只要按照max从小到大的顺序进行合并就行
const int maxn = 30001;
int maxval[maxn];
bool cmp(vector<int> & a, vector<int> & b){
    int max_vala = max(maxval[a[0]], maxval[a[1]]);
    int max_valb = max(maxval[b[0]], maxval[b[1]]);
    return max_vala < max_valb;
}
class Solution {
public:
    int father[maxn];
    int maxcnt[maxn];
    void initSet(int n, vector<int> & vals){
        for (int i = 0;i<n;i++){
            father[i] = i;
            maxval[i] = vals[i];
            maxcnt[i] = 1;
        }
    }
    int findSet(int x){
        if (x != father[x]){
            father[x] = findSet(father[x]);
        }
        return father[x];
    }
    //返回这次合并产生的好路径
    int unionSet(int x, int y){
        int path = 0;
        int fx = findSet(x);
        int fy = findSet(y);
        if (fx != fy){
            if (maxval[fx] > maxval[fy]){
                father[fy] = fx;
            }
            else if (maxval[fx] < maxval[fy]){
                father[fx] = fy;
            }
            else{
                path += maxcnt[fx] * maxcnt[fy];
                father[fx] = fy;
                maxcnt[fy] += maxcnt[fx];
            }
        }
        return path;
    }
    int numberOfGoodPaths(vector<int>& vals, vector<vector<int>>& edges) {
        int n = vals.size();
        initSet(n, vals);
        sort(edges.begin(), edges.end(), cmp);
        int m = edges.size();
        int ans = 0;
        for (int i = 0;i<m;i++){
            ans += unionSet(edges[i][0], edges[i][1]);
        }
        return ans + n;
    }
};
```

## [leetcode No.928 尽量减少恶意软件的传播II](https://leetcode.cn/problems/minimize-malware-spread-ii/description/)

给定一个由 `n` 个节点组成的网络，用 `n x n` 个邻接矩阵 `graph` 表示。在节点网络中，只有当 `graph[i][j] = 1` 时，节点 `i` 能够直接连接到另一个节点 `j`。

一些节点 `initial` 最初被恶意软件感染。只要两个节点直接连接，且其中至少一个节点受到恶意软件的感染，那么两个节点都将被恶意软件感染。这种恶意软件的传播将继续，直到没有更多的节点可以被这种方式感染。

假设 `M(initial)` 是在恶意软件停止传播之后，整个网络中感染恶意软件的最终节点数。

我们可以从 `initial` 中 **删除一个节点**，**并完全移除该节点以及从该节点到任何其他节点的任何连接。**

请返回移除后能够使 `M(initial)` 最小化的节点。如果有多个节点满足条件，返回索引 **最小的节点** 。



**示例 1：**

```
输入：graph = [[1,1,0],[1,1,0],[0,0,1]], initial = [0,1]
输出：0
```

**示例 2：**

```
输入：graph = [[1,1,0],[1,1,1],[0,1,1]], initial = [0,1]
输出：1
```

**示例 3：**

```
输入：graph = [[1,1,0,0],[1,1,1,0],[0,1,1,1],[0,0,1,1]], initial = [0,1]
输出：1
```



**提示：**

- `n == graph.length`
- `n == graph[i].length`
- `2 <= n <= 300`
- `graph[i][j]` 是 `0` 或 `1`.
- `graph[i][j] == graph[j][i]`
- `graph[i][i] == 1`
- `1 <= initial.length < n`
- `0 <= initial[i] <= n - 1`
-  `initial` 中每个整数都**不同**

![1c398e0e20f66c570d88ea8f44be285f_720](/assets/notes/zuoshen/union-find-05.jpg)

```cpp
const int maxn = 301;
//思路1.普通点合并
//    2. 有毒点最近的点进行标记
//    3.计算能拯救的点数
//代表元素（不包括有毒的）的标签: virus[maxn]来判断是否是源头，setsize[maxn]记录集合元素个数，origin[maxn]来标记 -1：没有源头，>=0：源头是origin[i]，-2：被多个源头侵染，没救了，cnts[maxn]:每个源头点删掉的话能拯救多少点
class Solution {
public:
//集合一定只放普通点，源头点根本不参与，也不是元素
    int father[maxn];
    bool virus[maxn] = {false};
    int setsize[maxn];
    int origin[maxn];
    int cnts[maxn];
    void initSet(int n, vector<int> & initial){
        for (int i = 0;i<n;i++){
            father[i] = i;
            setsize[i] = 1;
            origin[i] = -1;
            cnts[i] = 0;
        }
        for (int i : initial){
            virus[i] = true;
        }
    }
    int findSet(int x){
        if (x != father[x]){
            father[x] = findSet(father[x]);
        }
        return father[x];
    }
    void unionSet(int x, int y){
        int fx = findSet(x);
        int fy = findSet(y);
        if (fx != fy){
            father[fx] = fy;
            setsize[fy]++;
        }
    }
    int minMalwareSpread(vector<vector<int>>& graph, vector<int>& initial) {
        int n = graph.size();
        initSet(n, initial);
        for (int i = 0; i<n;i++){
            for (int j = i + 1; j<n;j++){
                if (graph[i][j] == 1 && !virus[i] && !virus[j]){
                    unionSet(i, j);
                }
            }
        }
        //病毒周围的普通点
        for (int item : initial){
            for (int neighbor = 0;neighbor<n;neighbor++){
                if(item != neighbor && !virus[neighbor] && graph[item][neighbor] == 1){
                    int fn = findSet(neighbor);
                    if (origin[fn] == -1){
                        origin[fn] = item;
                    }
                    else if (origin[fn] != -2 && origin[fn] != item){
                        origin[fn] = -2;
                    }
                }
            }
        }
        //只讨论代表点，其他的不看
        for(int i = 0;i<n;i++){
            if (i == findSet(i) && origin[i] >= 0){
                cnts[origin[i]] += setsize[i];
            }
        }
        sort(initial.begin(), initial.end());
        int ans = initial[0];
        int max_val = cnts[ans];
        for (int item : initial){
            if (cnts[item] > max_val){
                ans = item;
                max_val = cnts[item];
            }
        }
        return ans;
    }
};
```
