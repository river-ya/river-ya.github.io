# 建图、链式前向星

![f5d870206a0f6eb26f13a6d0bb4fd146_720](/assets/notes/zuoshen/topological-sort-01.jpg)



```cpp
#include <bits/stdc++.h>
using namespace std;
//点的最大数量
const int maxn = 11;
//边的最大数量
const int maxm = 21;
//只有链式前向星方式建图需要这个数量
//注意如果无向图的最大数量是m条边，数量要准备m * 2
//因为一条无向边要加两条有向边

//邻接矩阵方式建图
int graph1[maxn][maxn];

//邻接表方式建图（带权），如果不带权，把pair换成int即可
vector<vector<pair<int, int>>> graph2(maxn);

//链式前向星方式建图
int head[maxn];//下标是点号，val是头边号
int nxt[maxm];//下标是边号，val是下一条边号
int to[maxm];//下标是边号，val是下一个点号
//如果有权重
int weight[maxm];
//边的边号从哪开始
int cnt;

void init(int n){
	//邻接矩阵清空
	for (int i = 0;i<=n;i++){//注意开头的0下标往往不使用，从1开始作为第一个点标号
		for (int j = 0;j<=n;j++){
			graph1[i][j] = 0;
		}
	}
	//邻接表清空和准备
	graph2.assign(n + 1, vector<pair<int, int>>());
	//链式前向星清空
	cnt = 1;
	for (int i = 0;i<=n;i++){
		head[i] = 0;
	}
}

//链式前向星加边
void addEdge(int u, int v, int w){
	//u -> v, 权重 w
	nxt[cnt] = head[u];
	to[cnt] = v;
	weight[cnt] = w;
	head[u] = cnt++;
}

//三种方式建立有向图带权图
void directGraph(vector<vector<int>> & edges){
	//邻接矩阵建图
	for(auto & edge : edges){
		graph1[edge[0]][edge[1]] = edge[2];
	}
	//邻接表建图
	for (auto & edge : edges){
		graph2[edge[0]].emplace_back(edge[1], edge[2]);
	}
	//链式前向星建图
	for(auto & edge : edges){
		addEdge(edge[0], edge[1], edge[2]);
	}
}

//三种方式建立无向图带权图
void undirectGraph(vector<vector<int>> & edges) {
	//邻接矩阵建图
	for(auto & edge : edges){
		graph1[edge[0]][edge[1]] = edge[2];
		graph1[edge[1]][edge[0]] = edge[2];
	}
	//邻接表建图
	for (auto & edge : edges){
		graph2[edge[0]].emplace_back(edge[1], edge[2]);
		graph2[edge[1]].emplace_back(edge[0], edge[2]);
	}
	//链式前向星建图
	for (auto & edge : edges){
		addEdge(edge[0], edge[1], edge[2]);
		addEdge(edge[1], edge[0], edge[2]);
	}
}

void traversal(int n){
	//邻接矩阵遍历
	for (int i = 1;i<=n;i++){
		for (int j = 1;j<=n;j++){
			cout << graph1[i][j] << ' ';
		}
		cout << endl;
	}
	//邻接表遍历
	for (int i = 1;i<=n;i++){
		for(auto & edge : graph2[i]){
			cout << edge.first << " " << edge.second;
		}
		cout << endl;
	}
	//链式前向星遍历
	for(int i = 1; i<=n;i++){
		for (int ei = head[i]; ei > 0; ei = nxt[ei]){
			cout << to[ei] << ' ' << weight[ei];
		}
		cout << endl;
	}
}
```

# 拓扑排序

有向图、没有环

没有入度为0的点，那么这个图是循环依赖的

步骤：

1. 在图中找到所有入度为0的点

2. 把所有入度为0的点在图中删掉，重点是删掉影响！继续找到入度为0的点并删掉影响

3. 直到所有点都被删掉，依次删除的顺序就是正确的拓扑排序结果

4. 如果无法把所有的点都删掉，说明有向图里有环

## [leetcode No.207 课程表](https://leetcode.cn/problems/course-schedule/)

你这个学期必须选修 `numCourses` 门课程，记为 `0` 到 `numCourses - 1` 。

在选修某些课程之前需要一些先修课程。 先修课程按数组 `prerequisites` 给出，其中 `prerequisites[i] = [ai, bi]` ，表示如果要学习课程 `ai` 则 **必须** 先学习课程 `bi` 。

- 例如，先修课程对 `[0, 1]` 表示：想要学习课程 `0` ，你需要先完成课程 `1` 。

请你判断是否可能完成所有课程的学习？如果可以，返回 `true` ；否则，返回 `false` 。



**示例 1：**

```
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。
```

**示例 2：**

```
输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
输出：false
解释：总共有 2 门课程。学习课程 1 之前，你需要先完成课程 0 ；并且学习课程 0 之前，你还应先完成课程 1 。这是不可能的。
```



**提示：**

- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- `prerequisites[i]` 中的所有课程对 **互不相同**

```cpp
const int maxn = 2001;
const int maxm = 2001 * 2000;
class Solution {
public:
    int head[maxn];
    int nxt[maxm];
    int to[maxm];
    int cnt;
    void init(int n){
        for (int i = 0;i<n;i++){
            head[i] = 0;
        }
        cnt = 1;
    }
    void addEdge(int u, int v){
        nxt[cnt] = head[u];
        to[cnt] = v;
        head[u] = cnt++;
    }
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        init(numCourses);
        vector<int> indegree(numCourses, 0);
        for (auto & edge : prerequisites){
            addEdge(edge[1], edge[0]);
            indegree[edge[0]]++;//图和入度表同时建立
        }
        vector<int> que(numCourses, 0);
        int l = 0, r = 0;
        //先把入度为0的结点放进队列
        for (int i = 0;i<numCourses;i++){
            if (indegree[i] == 0){
                que[r++] = i;
            }
        }
        int counts = 0;
        while (l < r){
            int cur = que[l++];
            counts++;
            for (int ei = head[cur]; ei > 0; ei = nxt[ei]){
                if (--indegree[to[ei]] == 0){//注意ei表示的是边标号
                    que[r++] = to[ei];
                }
            }
        }
        vector<int> ans;
        return counts == numCourses ? que : ans;
    }
};
```

## [luogu 拓扑排序模板](https://www.luogu.com.cn/problem/U107394)

有向无环图上有n个点，m条边。求这张图字典序最小的拓扑排序的结果。字典序最小指希望排好序的结果中，比较靠前的数字尽可能小。

输入格式

第一行是用空格隔开的两个整数n和m，表示n个点和m条边。

接下来是m行，每行用空格隔开的两个数u和v，表示有一条从u到v的边。

输出格式

输出一行，拓扑排序的结果，数字之间用空格隔开

输入输出样例

**输入 #1**

```
5 3
1 2
2 4
4 3
```

**输出 #1**

```
1 2 4 3 5
```

说明/提示

1≤*n*,*m*≤105

注意：图上可能有重边

```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn = 100001;
const int maxm = 100001;
int head[maxn];
int nxt[maxm];
int to[maxm];
int cnt;
void addEdge(int u, int v){
    nxt[cnt] = head[u];
    to[cnt] = v;
    head[u] = cnt++;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cnt = 1;
    int n, m;
    cin >> n >> m;
    vector<int> indegree(n + 1, 0);
    for (int i = 0;i<m;i++){
        int x, y;
        cin >> x >> y;
        addEdge(x, y);
        indegree[y]++;
    }
    priority_queue<int, vector<int>, greater<int>> ans;
    for (int i = 1;i<=n;i++){
        if (indegree[i] == 0){
            ans.push(i);
        }
    }
    while (!ans.empty()){
        int cur = ans.top();
        ans.pop();
        cout << cur << ' ';
        for (int ei = head[cur]; ei > 0; ei = nxt[ei]){
            if (--indegree[to[ei]] == 0){
                ans.push(to[ei]);
            }
        }
    }
    return 0;
}
```

## [leetcode 火星词典](https://leetcode.cn/problems/Jf1JuT/description/)

现有一种使用英语字母的外星文语言，这门语言的字母顺序与英语顺序不同。

给定一个字符串列表 `words` ，作为这门语言的词典，`words` 中的字符串已经 **按这门新语言的字母顺序进行了排序** 。

请你根据该词典还原出此语言中已知的字母顺序，并 **按字母递增顺序** 排列。若不存在合法字母顺序，返回 `""` 。若存在多种可能的合法字母顺序，返回其中 **任意一种** 顺序即可。

字符串 `s` **字典顺序小于** 字符串 `t` 有两种情况：

- 在第一个不同字母处，如果 `s` 中的字母在这门外星语言的字母顺序中位于 `t` 中字母之前，那么 `s` 的字典顺序小于 `t` 。
- 如果前面 `min(s.length, t.length)` 字母都相同，那么 `s.length < t.length` 时，`s` 的字典顺序也小于 `t` 。



**示例 1：**

```
输入：words = ["wrt","wrf","er","ett","rftt"]
输出："wertf"
```

**示例 2：**

```
输入：words = ["z","x"]
输出："zx"
```

**示例 3：**

```
输入：words = ["z","x","z"]
输出：""
解释：不存在合法字母顺序，因此返回 ""。
```



**提示：**

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` 仅由小写英文字母组成

```cpp
const int maxn = 27;
const int maxm = 27;
class Solution {
public:
    int nxt[maxm];
    int head[maxn];
    int to[maxm];
    int cnt;
    void addEdge(int u, int v){
        nxt[cnt] = head[u];
        to[cnt] = v;
        head[u] = cnt++;
    }
    string alienOrder(vector<string>& words) {
        vector<int> indegree(26, -1);
        cnt = 1;
        for (string word : words){
            for(int i = 0;i<word.size();i++){
                indegree[word[i] - 'a'] = 0;//确定所有入度点
            }
        }
        for (int i = 0, j, len;i < words.size() - 1;i++){
            string cur = words[i];
            string next = words[i+1];
            j = 0;
            len = min(cur.size(), next.size());
            for (; j < len; j++){
                if (cur[j] != next[j]){
                    addEdge(cur[j] - 'a', next[j] - 'a');
                    indegree[next[j] - 'a']++;//建图并建入度表
                    break;
                }
            }
            //不合理的情况：cur = abcd, next = abc
            if (j < cur.size() && j == next.size()){
                return "";
            }
        }
        vector<int> que(26, 0);
        int l = 0, r = 0;
        int kinds = 0;
        for (int i = 0;i<26;i++){
            if (indegree[i] != -1){
                kinds++;
            }
            if (indegree[i] == 0){
                que[r++] = i;
            }
        }
        string ans = "";
        while (l < r){
            int cur = que[l++];
            ans += cur + 'a';
            for (int ei = head[cur]; ei > 0; ei = nxt[ei]){
                if (--indegree[to[ei]] == 0){
                    que[r++] = to[ei];
                }
            }
        }
        return ans.size() == kinds ? ans : "";
    }
};
```

## [leetcode No.936 戳印序列](https://leetcode.cn/problems/stamping-the-sequence/description/)

你想要用**小写字母**组成一个目标字符串 `target`。

开始的时候，序列由 `target.length` 个 `'?'` 记号组成。而你有一个小写字母印章 `stamp`。

在每个回合，你可以将印章放在序列上，并将序列中的每个字母替换为印章上的相应字母。你最多可以进行 `10 * target.length` 个回合。

举个例子，如果初始序列为 "?????"，而你的印章 `stamp` 是 `"abc"`，那么在第一回合，你可以得到 "abc??"、"?abc?"、"??abc"。（请注意，印章必须完全包含在序列的边界内才能盖下去。）

如果可以印出序列，那么返回一个数组，该数组由每个回合中被印下的最左边字母的索引组成。如果不能印出序列，就返回一个空数组。

例如，如果序列是 "ababc"，印章是 `"abc"`，那么我们就可以返回与操作 "?????" -> "abc??" -> "ababc" 相对应的答案 `[0, 2]`；

另外，如果可以印出序列，那么需要保证可以在 `10 * target.length` 个回合内完成。任何超过此数字的答案将不被接受。



**示例 1：**

```
输入：stamp = "abc", target = "ababc"
输出：[0,2]
（[1,0,2] 以及其他一些可能的结果也将作为答案被接受）
```

**示例 2：**

```
输入：stamp = "abca", target = "aabcaca"
输出：[3,0,1]
```



**提示：**

1. `1 <= stamp.length <= target.length <= 1000`
2. `stamp` 和 `target` 只包含小写字母。

```cpp
//类似于时光逆流，先找出最后覆盖的
const int maxn = 1005;
const int maxm = 100005;
int cnt;
class Solution {
public:
    int nxt[maxm];
    int to[maxm];
    int head[maxn];
    int indegree[maxn];
    void addEdge(int u, int v){
        nxt[cnt] = head[u];
        to[cnt] = v;
        head[u] = cnt++;
    }
    void init(int n){
        for (int i = 0;i<=n;i++){
            head[i] = 0;
        }
        cnt = 1;
    }
    vector<int> movesToStamp(string stamp, string target) {
        int n = target.size();
        init(n);
        int counts = 0;
        int m = stamp.size();
        for (int i = 0;i<n;i++){
            indegree[i] = m;
        }
        int r = 0, l = 0;
        vector<int> que(n - m + 1, 0);
        for (int i = 0; i < n - m + 1; i++){
            for (int j = 0; j < m;j++){
                if (target[i + j] == stamp[j]){
                    if(--indegree[i] == 0){
                        que[r++] = i;
                    }
                }
                else{
                    addEdge(i + j, i);//错误位置 -> i开头的下标
                }
            }
        }
        vector<bool> visited(n, false);//同一个位置取消错误不要重复统计
        while(l < r){
            int cur = que[l++];
            counts++;
            for (int i = 0;i<m;i++){
                if (!visited[cur + i]){
                    visited[cur + i] = true;
                    for (int ei = head[cur + i]; ei > 0; ei = nxt[ei]){
                        if (--indegree[to[ei]] == 0){
                            que[r++] = to[ei];
                        }
                    }
                }
            }
        }
        if (counts == que.size()){
            reverse(que.begin(), que.end());
            return que;
        }
        else{
            vector<int> ans;
            return ans;
        }
    }
};
```

## [luogu P4017 最大食物链计数](https://www.luogu.com.cn/problem/P4017)

P4017 最大食物链计数

题目背景

你知道食物链吗？Delia 生物考试的时候，数食物链条数的题目全都错了，因为她总是重复数了几条或漏掉了几条。于是她来就来求助你，然而你也不会啊！写一个程序来帮帮她吧。

题目描述

给你一个食物网，你要求出这个食物网中最大食物链的数量。

（这里的“最大食物链”，指的是**生物学意义上的食物链**，即**最左端是不会捕食其他生物的生产者，最右端是不会被其他生物捕食的消费者**。）

Delia 非常急，所以你只有 $1$ 秒的时间。

由于这个结果可能过大，你只需要输出总数模上 $80112002$ 的结果。

输入格式

第一行，两个正整数 $n$、$m$，表示生物种类 $n$ 和吃与被吃的关系数 $m$。

接下来 $m$ 行，每行两个正整数，表示被吃的生物 A 和吃 A 的生物 B。

输出格式

一行一个整数，为最大食物链数量模上 $80112002$ 的结果。

输入输出样例 #1

输入 #1

```
5 7
1 2
1 3
2 3
3 5
2 5
4 5
3 4
```

输出 #1

```
5
```

说明/提示

各测试点满足以下约定：

| 测试点编号 |        $n$         |        $m$         |
| :--------: | :----------------: | :----------------: |
|   $1,2$    |      $\le 40$      |     $\le 400$      |
|   $3,4$    |     $\le 100$      | $\le 2\times 10^3$ |
|   $5,6$    |     $\le 10^3$     | $\le 6\times 10^4$ |
|   $7,8$    | $\le 2\times 10^3$ | $\le 2\times 10^5$ |
|   $9,10$   | $\le 5\times 10^3$ | $\le 5\times 10^5$ |

对于 $100\%$ 的数据，$1 \le n \le 5\times 10^3,1\le m \le 5\times 10^5$

【补充说明】

数据中不会出现环，满足生物学的要求。（感谢 @AKEE）

```cpp
#include <bits/stdc++.h>
using namespace std;
int n, m;
const int maxn = 5005;
const int maxm = 500005;
const int mod = 80112002;
int to[maxm];
int nxt[maxm];
int head[maxn];
int message[maxn];//新增一个信息数组
int cnt = 0;
void addEdge(int u, int v){
	nxt[cnt] = head[u];
	to[cnt] = v;
	head[u] = cnt++;
}
int main(){
	cnt = 1;
	cin >> n >> m;
	vector<int> indegree(n + 1, 0);
	for (int i = 0;i<m;i++){
		int x, y;
		cin >> x >> y;
		addEdge(x, y);
		indegree[y]++;
	}
	vector<int> que(n, 0);
	int l = 0, r = 0;
	for (int i = 1;i<=n;i++){
		if (indegree[i] == 0){
			que[r++] = i;
			message[i] = 1;//最底层开始有1条链
		}
	}
	int ans = 0;
	while (l < r){
		int cur = que[l++];
		if (head[cur] == 0){
			//当前节点出度为0
			ans = (ans + message[cur]) % mod;
		}
		for (int ei = head[cur]; ei > 0; ei = nxt[ei]){
			message[to[ei]] = (message[to[ei]] + message[cur]) % mod;
			if (--indegree[to[ei]] == 0){
				que[r++] = to[ei];
			}
		}
	}
	cout << ans;
}
```

## [leetcode No.851 喧闹和富有](https://leetcode.cn/problems/loud-and-rich/)

有一组 `n` 个人作为实验对象，从 `0` 到 `n - 1` 编号，其中每个人都有不同数目的钱，以及不同程度的安静值（quietness）。为了方便起见，我们将编号为 `x` 的人简称为 "person `x` "。

给你一个数组 `richer` ，其中 `richer[i] = [ai, bi]` 表示 person `ai` 比 person `bi` 更有钱。另给你一个整数数组 `quiet` ，其中 `quiet[i]` 是 person `i` 的安静值。`richer` 中所给出的数据 **逻辑自洽**（也就是说，在 person `x` 比 person `y` 更有钱的同时，不会出现 person `y` 比 person `x` 更有钱的情况 ）。

现在，返回一个整数数组 `answer` 作为答案，其中 `answer[x] = y` 的前提是，在所有拥有的钱肯定不少于 person `x` 的人中，person `y` 是最不安静的人（也就是安静值 `quiet[y]` 最小的人）。



**示例 1：**

```
输入：richer = [[1,0],[2,1],[3,1],[3,7],[4,3],[5,3],[6,3]], quiet = [3,2,5,4,6,1,7,0]
输出：[5,5,2,5,4,5,6,7]
解释：
answer[0] = 5，
person 5 比 person 3 有更多的钱，person 3 比 person 1 有更多的钱，person 1 比 person 0 有更多的钱。
唯一较为安静（有较低的安静值 quiet[x]）的人是 person 7，
但是目前还不清楚他是否比 person 0 更有钱。
answer[7] = 7，
在所有拥有的钱肯定不少于 person 7 的人中（这可能包括 person 3，4，5，6 以及 7），
最安静（有较低安静值 quiet[x]）的人是 person 7。
其他的答案也可以用类似的推理来解释。
```

**示例 2：**

```
输入：richer = [], quiet = [0]
输出：[0]
```



**提示：**

- `n == quiet.length`
- `1 <= n <= 500`
- `0 <= quiet[i] < n`
- `quiet` 的所有值 **互不相同**
- `0 <= richer.length <= n * (n - 1) / 2`
- `0 <= ai, bi < n`
- `ai != bi`
- `richer` 中的所有数对 **互不相同**
- 对 `richer` 的观察在逻辑上是一致的

```cpp
const int maxn = 505;
const int maxm = 250000;
class Solution {
public:
	int to[maxm];
	int nxt[maxm];
	int head[maxn];
	int cnt;
	void init(int n){
		for (int i = 0;i<n;i++){
			head[i] = 0;
		}
		cnt = 1;
	}
	void addEdge(int u, int v){
		nxt[cnt] = head[u];
		to[cnt] = v;
		head[u] = cnt++;
	}
    vector<int> loudAndRich(vector<vector<int>>& richer, vector<int>& quiet) {
        int n = quiet.size();
        int m = richer.size();
        init(n);
        vector<int> indegree(n, 0);
        for (auto ele : richer){
            addEdge(ele[0], ele[1]);
            indegree[ele[1]]++;
		}
		vector<int> que(n, 0);
		int l = 0, r= 0;
		vector<int> ans(n, 0);
		for (int i = 0;i<n;i++){
			if (indegree[i] == 0){
				que[r++] = i;
			}
			ans[i] = i;//一开始默认自己是最小
		}
		while (l < r){
			int cur = que[l++];
			for (int ei = head[cur]; ei > 0; ei = nxt[ei]){
				if (quiet[ans[to[ei]]] > quiet[ans[cur]]){
					ans[to[ei]] = ans[cur];//注意只比较答案处的quiet不用修改，但是修改答案必须两边同时作用ans
				}
				if (--indegree[to[ei]] == 0){
					que[r++] = to[ei];
				}//不要忘了入度--
			}
		}
		return ans;
    }
};
```

## [leetcode No.2050 并行课程 III](https://leetcode.cn/problems/parallel-courses-iii/description/)

给你一个整数 `n` ，表示有 `n` 节课，课程编号从 `1` 到 `n` 。同时给你一个二维整数数组 `relations` ，其中 `relations[j] = [prevCoursej, nextCoursej]` ，表示课程 `prevCoursej` 必须在课程 `nextCoursej` **之前** 完成（先修课的关系）。同时给你一个下标从 **0** 开始的整数数组 `time` ，其中 `time[i]` 表示完成第 `(i+1)` 门课程需要花费的 **月份** 数。

请你根据以下规则算出完成所有课程所需要的 **最少** 月份数：

- 如果一门课的所有先修课都已经完成，你可以在 **任意** 时间开始这门课程。
- 你可以 **同时** 上 **任意门课程** 。

请你返回完成所有课程所需要的 **最少** 月份数。

**注意：**测试数据保证一定可以完成所有课程（也就是先修课的关系构成一个有向无环图）。



**示例 1:**

**![img](https://assets.leetcode.com/uploads/2021/10/07/ex1.png)**

```
输入：n = 3, relations = [[1,3],[2,3]], time = [3,2,5]
输出：8
解释：上图展示了输入数据所表示的先修关系图，以及完成每门课程需要花费的时间。
你可以在月份 0 同时开始课程 1 和 2 。
课程 1 花费 3 个月，课程 2 花费 2 个月。
所以，最早开始课程 3 的时间是月份 3 ，完成所有课程所需时间为 3 + 5 = 8 个月。
```

**示例 2：**

**![img](https://assets.leetcode.com/uploads/2021/10/07/ex2.png)**

```
输入：n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
输出：12
解释：上图展示了输入数据所表示的先修关系图，以及完成每门课程需要花费的时间。
你可以在月份 0 同时开始课程 1 ，2 和 3 。
在月份 1，2 和 3 分别完成这三门课程。
课程 4 需在课程 3 之后开始，也就是 3 个月后。课程 4 在 3 + 4 = 7 月完成。
课程 5 需在课程 1，2，3 和 4 之后开始，也就是在 max(1,2,3,7) = 7 月开始。
所以完成所有课程所需的最少时间为 7 + 5 = 12 个月。
```



**提示：**

- `1 <= n <= 5 * 104`
- `0 <= relations.length <= min(n * (n - 1) / 2, 5 * 104)`
- `relations[j].length == 2`
- `1 <= prevCoursej, nextCoursej <= n`
- `prevCoursej != nextCoursej`
- 所有的先修课程对 `[prevCoursej, nextCoursej]` 都是 **互不相同** 的。
- `time.length == n`
- `1 <= time[i] <= 104`
- 先修课程图是一个有向无环图。

## [leetcode No.2127 参加会议的最多员工数](https://leetcode.cn/problems/maximum-employees-to-be-invited-to-a-meeting/)

一个公司准备组织一场会议，邀请名单上有 `n` 位员工。公司准备了一张 **圆形** 的桌子，可以坐下 **任意数目** 的员工。

员工编号为 `0` 到 `n - 1` 。每位员工都有一位 **喜欢** 的员工，每位员工 **当且仅当** 他被安排在喜欢员工的旁边，他才会参加会议。每位员工喜欢的员工 **不会** 是他自己。

给你一个下标从 **0** 开始的整数数组 `favorite` ，其中 `favorite[i]` 表示第 `i` 位员工喜欢的员工。请你返回参加会议的 **最多员工数目** 。



**示例 1：**

![img](https://assets.leetcode.com/uploads/2021/12/14/ex1.png)

```
输入：favorite = [2,2,1,2]
输出：3
解释：
上图展示了公司邀请员工 0，1 和 2 参加会议以及他们在圆桌上的座位。
没办法邀请所有员工参与会议，因为员工 2 没办法同时坐在 0，1 和 3 员工的旁边。
注意，公司也可以邀请员工 1，2 和 3 参加会议。
所以最多参加会议的员工数目为 3 。
```

**示例 2：**

```
输入：favorite = [1,2,0]
输出：3
解释：
每个员工都至少是另一个员工喜欢的员工。所以公司邀请他们所有人参加会议的前提是所有人都参加了会议。
座位安排同图 1 所示：
- 员工 0 坐在员工 2 和 1 之间。
- 员工 1 坐在员工 0 和 2 之间。
- 员工 2 坐在员工 1 和 0 之间。
参与会议的最多员工数目为 3 。
```

**示例 3：**

![img](https://assets.leetcode.com/uploads/2021/12/14/ex2.png)

```
输入：favorite = [3,0,1,4,1]
输出：4
解释：
上图展示了公司可以邀请员工 0，1，3 和 4 参加会议以及他们在圆桌上的座位。
员工 2 无法参加，因为他喜欢的员工 1 旁边的座位已经被占领了。
所以公司只能不邀请员工 2 。
参加会议的最多员工数目为 4 。
```



**提示：**

- `n == favorite.length`
- `2 <= n <= 105`
- `0 <= favorite[i] <= n - 1`
- `favorite[i] != i`

![48731cf20cc180c5792700a7dbf2a113_720](/assets/notes/zuoshen/topological-sort-02.jpg)

![a7b89aec90d94c49830507c382bc920d_720](/assets/notes/zuoshen/topological-sort-03.jpg)

![6f0cf43402825d721d97c9e0ca97b70a_720](/assets/notes/zuoshen/topological-sort-04.jpg)

```cpp
//favorite就表示图，不需要额外建图 favorite[a] = b ： a -> b
//此题一定有环
//smallring : 可以两边延申最大长度
//bigring: 只能放环里的
//然后pk
//本题实际上是基环树
class Solution {
public:
    int maximumInvitations(vector<int>& favorite) {
        int n = favorite.size();
        vector<int> indegree(n, 0);
        for(int i = 0;i<n;i++){
            indegree[favorite[i]]++;
        }
        vector<int> que(n, 0);
        int l = 0, r = 0;
        for (int i = 0;i<n;i++){
            if (indegree[i] == 0){
                que[r++] = i;
            }
        }
        // deep[i] : 不包括i在内，i之前的最长链长度
        vector<int> deep(n, 0);
        while (l < r){
            int cur = que[l++];
            int next = favorite[cur];
            deep[next] = max(deep[cur] + 1, deep[next]);
            if (--indegree[next] == 0){
                que[r++] = next;
            }
        }
        // 目前图中的点，不在环上的都删除了
        // indegree[i] == 0 即被删除
        //可能性1 : 所有小环（中心个数 == 2）算上中心点 + 延伸点，总个数
        int sum_of_small_rings = 0;
        // 可能性2 ： 所有大环（中心个数 > 2）只算中心点，最大环的中心点个数
        int big_rings = 0;
        for (int i = 0;i<n;i++){
            if (indegree[i] > 0){
                int ringsize = 1;
                indegree[i] = 0;
                for (int j = favorite[i]; j != i; j = favorite[j]){
                    ringsize++;
                    indegree[j] = 0;
                }
                if (ringsize == 2){
                    sum_of_small_rings += deep[i] + 2 + deep[favorite[i]];
                }
                else{
                    big_rings = max(ringsize, big_rings);
                }
            }
        }
        return max(big_rings, sum_of_small_rings);
    }
};
```
