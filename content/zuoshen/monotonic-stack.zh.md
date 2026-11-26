# 单调栈

单调栈最经典的用法是解决如下问题：
每个位置都求：
1）当前位置的左侧比当前位置的数字小，且距离最近的位置在哪

2）当前位置的右侧比当前位置的数字小，且距离最近的位置在哪

栈[ 小-----> 大 ]

或者

每个位置都求：
1）当前位置的左侧比当前位置的数字大，且距离最近的位置在哪

2）当前位置的右侧比当前位置的数字大，且距离最近的位置在哪

栈[大 -------> 小]

## nowcoder 单调栈结构(进阶)

[原题](https://www.nowcoder.com/practice/2a2c00e7a88a498693568cef63a4b7bb)

给定一个可能含有重复值的数组 arr，找到每一个 i 位置左边和右边离 i 位置最近且值比 arr[i] 小的位置。返回所有位置相应的信息。

https://in.mesl.cloud/#/register?code=zhMdz5sh

```cpp
#include<bits/stdc++.h>
using namespace std;
int n;
vector<int> nums;
const int maxn = 1000001;
int stk[maxn];
int ans[maxn][2];
int main(){
	cin >> n;
	nums.assign(n, 0);
	for (int i = 0; i<n;i++){
		cin >> nums[i];
	}
	int r = 0;
	int cur;
	//遍历阶段
	for (int i = 0; i<n;i++){
		while(r > 0 && nums[stk[r-1]] >= nums[i]){
			cur = stk[--r]; // 下标
			ans[cur][0] = r > 0 ? stk[r-1] : -1;
			ans[cur][1] = i;
		}
		stk[r++] = i;
	}
	// 清算阶段
	while(r > 0){
		cur = stk[--r];
		ans[cur][0] = r > 0 ? stk[r-1] : -1;
		ans[cur][1] = -1;
	}
	// 修正阶段
	// 左侧答案一定是正确的，右侧答案可能需要传递
	// 从右往左修正
	for (int i = n - 2; i>=0;i--){
		if(ans[i][1] != -1 && nums[ans[i][1]] == nums[i]){
			ans[i][1] = ans[ans[i][1]][1];
		}
	}
	for (int i = 0; i<n;i++){
		cout << ans[i][0] << ' ' << ans[i][1] << '\n';
	}

}
```

## leetcode LCR 038. 每日温度

[原题](https://leetcode.cn/problems/iIQa4I/description/)

请根据每日 `气温` 列表 `temperatures` ，重新生成一个列表，要求其对应位置的输出为：要想观测到更高的气温，至少需要等待的天数。如果气温在这之后都不会升高，请在该位置用 `0` 来代替。



**示例 1：**

```
输入：temperatures = [73,74,75,71,69,72,76,73]
输出：[1,1,4,2,1,1,0,0]
```

**示例 2：**

```
输入：temperatures = [30,40,50,60]
输出：[1,1,1,0]
```

**示例 3：**

```
输入：temperatures = [30,60,90]
输出：[1,1,0]
```



**提示：**

- `1 <= temperatures.length <= 105`
- `30 <= temperatures[i] <= 100`

```cpp
class Solution {
public:
	//相当于求右侧离该位置最近的比当前大的数的位置，然后再遍历一遍数组求  数组的值-当前下标
    vector<int> dailyTemperatures(vector<int>& tem) {
		int n = tem.size();
		// 遍历阶段
		// 小压大
		const int maxn = 100001;
		int stk[maxn];
		vector<int> ans(n, 0); // 右侧
		int cur;
		int r = 0;
		for (int i = 0; i<n;i++){
			while (r > 0 && tem[i] >= tem[stk[r-1]]){
				cur = stk[--r];
				ans[cur] = i;
			}
			stk[r++] = i;
		}
		// 清算阶段
		while (r > 0)
		{
			cur = stk[--r];
			ans[cur] = -1;
		}
		// 修正阶段
		for (int i = n - 2; i >=0; i--){
			if(ans[i] != -1 && tem[ans[i]] == tem[i]){
				ans[i] = ans[ans[i]];
			}
		}
		for(int i = 0; i<n;i++){
            if(ans[i] != -1){
                ans[i] -= i;
            }
            else{
                ans[i] = 0;
            }
		}
		return ans;
    }
};
```

## leetcode 907. 子数组的最小值之和

[原题](https://leetcode.cn/problems/sum-of-subarray-minimums/description/)

给定一个整数数组 `arr`，找到 `min(b)` 的总和，其中 `b` 的范围为 `arr` 的每个（连续）子数组。

由于答案可能很大，因此 **返回答案模 `10^9 + 7`** 。



**示例 1：**

```
输入：arr = [3,1,2,4]
输出：17
解释：
子数组为 [3]，[1]，[2]，[4]，[3,1]，[1,2]，[2,4]，[3,1,2]，[1,2,4]，[3,1,2,4]。
最小值为 3，1，2，4，1，1，2，1，1，1，和为 17。
```

**示例 2：**

```
输入：arr = [11,81,94,43,3]
输出：444
```



**提示：**

- `1 <= arr.length <= 3 * 104`
- `1 <= arr[i] <= 3 * 104`

```cpp
using ll = long long;
#define mod 1000000007
class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        int n = arr.size();
        ll ans = 0;
        const int maxn = 30005;
        int stk[maxn];
        // 遍历阶段
        int r = 0;
        int cur;
		for (int i = 0; i<n;i++){
			while(r > 0 && arr[i] <= arr[stk[r-1]]){
				cur = stk[--r];
				int left = r > 0 ? stk[r-1] : -1;
				ans = (ans + (ll)(cur - left) * (i - cur)  * arr[cur]) % mod;
			}
			stk[r++] = i;
		}
		// 清算阶段
		while (r > 0){
			cur = stk[--r];
			int left = r > 0 ? stk[r-1] : -1;
			ans = (ans + (ll)(cur - left) * (n - cur) * arr[cur]) % mod;
		}
		return (int)ans;
    }
};
```

## leetcode LCR 039. 柱状图中最大的矩形

[原题](https://leetcode.cn/problems/0ynMMM/description/)

给定非负整数数组 `heights` ，数组中的数字用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 `1` 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。



**示例 1:**

[原题配图](https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg)

```
输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10
```

**示例 2：**

[原题配图](https://assets.leetcode.com/uploads/2021/01/04/histogram-1.jpg)

```
输入： heights = [2,4]
输出： 4
```



**提示：**

- `1 <= heights.length <=105`
- `0 <= heights[i] <= 104`

```cpp
//套模板
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
		int n = heights.size();
		const int maxn = 100005;
		int stk[maxn];
		int ans[maxn][2];
		// 遍历阶段
		int r = 0;
		int cur;
		for (int i = 0; i<n;i++){
			while (r > 0 && heights[i] <= heights[stk[r-1]]){
				cur = stk[--r];
				ans[cur][0] = r > 0 ? stk[r-1] : -1;
				ans[cur][1] = i;
			}
			stk[r++] = i;
		}
		// 清算阶段
		while (r > 0){
			cur = stk[--r];
			ans[cur][0] = r > 0 ? stk[r-1] : -1;
			ans[cur][1] = n;
		}
		// 修正阶段
		for (int i = n - 2; i>=0;i--){
			if(ans[i][1] != n && heights[ans[i][1]] == heights[i]){
				ans[i][1] = ans[ans[i][1]][1];
			}
		}
		int s = 0;
		for (int i = 0; i<n;i++){
			s = max(heights[i] * (ans[i][1] - ans[i][0] - 1), s);
		}
		return s;
    }
};
//左神的版本，可以自动修正
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
		int n = heights.size();
		const int maxn = 100005;
		int stk[maxn];
		// 遍历阶段
		int r = 0;
		int cur;
		int s = 0;
		for (int i = 0; i<n;i++){
			while (r > 0 && heights[i] <= heights[stk[r-1]]){
				cur = stk[--r];
				int left = r > 0 ? stk[r-1] : -1;
				s = max(s, (i - left - 1) * heights[cur]);
			}
			stk[r++] = i;
		}
		// 清算阶段
		while (r > 0){
			cur = stk[--r];
			int left = r > 0 ? stk[r-1] : -1;
			s = max(s, (n - left - 1) * heights[cur]);
		}
		return s;
    }
};
```

## leetcode LCR 040. 最大矩形

[原题](https://leetcode.cn/problems/PLYXKQ/description/)

给定一个由 `0` 和 `1` 组成的矩阵 `matrix` ，找出只包含 `1` 的最大矩形，并返回其面积。

**注意：**此题 `matrix` 输入格式为一维 `01` 字符串数组。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2020/09/14/maximal.jpg)

```
输入：matrix = ["10100","10111","11111","10010"]
输出：6
解释：最大矩形如上图所示。
```

**示例 2：**

```
输入：matrix = []
输出：0
```

**示例 3：**

```
输入：matrix = ["0"]
输出：0
```

**示例 4：**

```
输入：matrix = ["1"]
输出：1
```

**示例 5：**

```
输入：matrix = ["00"]
输出：0
```



**提示：**

- `rows == matrix.length`
- `cols == matrix[0].length`
- `0 <= row, cols <= 200`
- `matrix[i][j]` 为 `'0'` 或 `'1'`

```cpp
class Solution {
public:
    int maximalRectangle(vector<string>& matrix) {
		// 0行为底的，1行为底的……
		int n = matrix.size();
        if(n == 0) return 0;
		int m = matrix[0].size();
		vector<int> arr(m, 0);
		const int maxn = 202;
		int stk[maxn] = {0};
		int s = 0;
		for (int i = 0; i<n;i++){
			int r = 0;
			int cur;
            arr.assign(m, 0);
			for (int j = 0;j<m;j++){
				for (int k = i; k>=0;k--){
					if (matrix[k][j] == '0'){
						break;
					}
					arr[j]++;
				}
				// 遍历阶段
				while(r > 0 && arr[j] <= arr[stk[r-1]]){
					cur = stk[--r];
					int left = r > 0 ? stk[r-1] : -1;
					s = max(s, (j - left - 1) * arr[cur]);
				}
				stk[r++] = j;
			}
			// 清算阶段
			while (r > 0){
				cur = stk[--r];
				int left = r > 0 ? stk[r-1] : -1;
				s = max(s, (m - left - 1) * arr[cur]);
			}
		}
		return s;
    }
};
//去掉k循环
class Solution {
public:
    int maximalRectangle(vector<string>& matrix) {
		// 0行为底的，1行为底的……
		int n = matrix.size();
        if(n == 0) return 0;
		int m = matrix[0].size();
		vector<int> arr(m, 0);
		const int maxn = 202;
		int stk[maxn] = {0};
		int s = 0;

		for (int i = 0; i<n;i++){
			int r = 0;
			int cur;
			for (int j = 0;j<m;j++){
				arr[j] = matrix[i][j] == '0' ? 0 : arr[j] + 1;
				// 遍历阶段
				while(r > 0 && arr[j] <= arr[stk[r-1]]){
					cur = stk[--r];
					int left = r > 0 ? stk[r-1] : -1;
					s = max(s, (j - left - 1) * arr[cur]);
				}
				stk[r++] = j;
			}
			// 清算阶段
			while (r > 0){
				cur = stk[--r];
				int left = r > 0 ? stk[r-1] : -1;
				s = max(s, (m - left - 1) * arr[cur]);
			}
		}
		return s;
    }
};
```

# 单调栈技巧

除了单调栈最经典的用法之外，在很多问题里单调栈还可以  **维持求解答案的可能性**

1）单调栈里的所有对象按照 **规定好的单调性来组织**

2）当某个对象进行单调栈时，会从 **栈顶开始** 依次淘汰单调栈里 **对后续求解答案没有帮助** 的对象

3）每个对象从栈顶弹出的时候 **结算当前对象参与的答案**， 随后这个对象 **不再参与后续求解答案的过程**

4）其实是 **先有对题目的分析**，进而**发现单调性**，然后利用**单调性的特征** 去实现

## leetcode 962. 最大宽度坡

[原题](https://leetcode.cn/problems/maximum-width-ramp/description/)

给定一个整数数组 `A`，*坡*是元组 `(i, j)`，其中 `i < j` 且 `A[i] <= A[j]`。这样的坡的宽度为 `j - i`。

找出 `A` 中的坡的最大宽度，如果不存在，返回 0 。



**示例 1：**

```
输入：[6,0,8,2,1,5]
输出：4
解释：
最大宽度的坡为 (i, j) = (1, 5): A[1] = 0 且 A[5] = 5.
```

**示例 2：**

```
输入：[9,8,1,0,1,9,4,0,4,1]
输出：7
解释：
最大宽度的坡为 (i, j) = (2, 9): A[2] = 1 且 A[9] = 1.
```



**提示：**

1. `2 <= A.length <= 50000`
2. `0 <= A[i] <= 50000`

```cpp
class Solution {
public:
    int maxWidthRamp(vector<int>& nums) {
        // 分析是否具备单调栈的特性
        // 左小右大
		// 第一个元素肯定要进栈，如果之后的元素比当前栈顶元素大，那么就没有必要进栈
		// 因为以栈顶元素为左边界的长度一定比新进入的元素长
		const int maxn = 50005;
		int stk[maxn];
		int s = 0;
		int n = nums.size();
		int r = 0;
		// 遍历阶段
		for (int i = 0; i < n;i++){
			if (r == 0 || nums[i] < nums[stk[r-1]]){
				stk[r++] = i;
			}
		}
        // 结算阶段，从右往左遍历如果有值大于等于栈顶元素对应值，那么之后栈顶元素一定不会继续构成更好的答案了，弹出
		for (int i = n - 1; i>=0;i--){
			while (r > 0 && nums[i] >= nums[stk[r-1]]){
				int cur = stk[--r];
				s = max(s, i - cur);
			}
			if (r == 0) break;
		}
		return s;
    }
};
```

## leetcode 316. 去除重复字母

[原题](https://leetcode.cn/problems/remove-duplicate-letters/description/)

给你一个字符串 `s` ，请你去除字符串中重复的字母，使得每个字母只出现一次。需保证 **返回结果的字典序最小**（要求不能打乱其他字符的相对位置）。



**示例 1：**

```
输入：s = "bcabc"
输出："abc"
```

**示例 2：**

```
输入：s = "cbacdcbc"
输出："acdb"
```



**提示：**

- `1 <= s.length <= 104`
- `s` 由小写英文字母组成

```cpp
class Solution {
public:
    string removeDuplicateLetters(string s) {
        // 统计词频
		int word[26] = {0};
		int enter[26] = {0};
		int n = s.size();
		for (int i = 0; i<n;i++){
			word[s[i] - 'a']++;
		}
		const int maxn = 10005;
		char stk[maxn];
		// 初始化
		stk[0] = s[0];
		int r = 1;
        enter[s[0] - 'a']++;
        word[s[0] - 'a']--;
		// 遍历阶段
		for (int i = 1; i<n;i++){
			// 已经进入过了，直接跳过
            if (enter[s[i] -'a']){
                word[s[i] - 'a']--;
                continue;
            }
			while (r > 0 && s[i] <= stk[r-1] && word[stk[r-1] - 'a'] > 0){
                enter[stk[--r] -  'a']--;
			}
			stk[r++] = s[i];
            word[s[i] - 'a']--;
            enter[s[i] - 'a']++;
		}
		//清算阶段
		string ans = "";
		for (int i = 0; i<r;i++){
			ans += stk[i];
		}
		return ans;
    }
};
```

## leetcode 大鱼吃小鱼

[原题](https://www.nowcoder.com/practice/3fdfc63015df42c6a78fdae46709fa69?tpId=0)

牛牛最近喜欢上了俄罗斯套娃、大鱼吃小鱼这些大的包住小的类型的游戏。

于是牛爸给牛牛做了一个特别版的大鱼吃小鱼游戏，他希望通过这个游戏
能够近一步提高牛牛的智商。
游戏规则如下：

- 现在有N条鱼，每条鱼的体积为Ai，从左到右排成一排。
- A数组是一个排列。
- 牛牛每轮可以执行一次大鱼吃小鱼的操作
- 一次大鱼吃小鱼的操作：对于每条鱼，它在每一次操作时会吃掉右边比自己小的第一条鱼
- 值得注意的时，在一次操作中，每条鱼吃比自己小的鱼的时候是同时发生的。
- 举一个例子，假设现在有三条鱼,体积为分别[5，4，3]，5吃4，4吃3，一次操作后就剩下[5]一条鱼。
  牛爸问牛牛，你知道要多少次操作，鱼的数量就不会变了嘛？

输出：表示要多少次操作，鱼的数量就不会变了

```cpp
class Solution {
public:
    int solve(int n, vector<int>& arr) {
        //弹出的时候，接替对方的工作
		 const int maxn = 100001;
		 int stk[maxn][2];
		 // 二维栈， （体重，轮数）
		 int r = 0;
		 int ans = 0;
		 for (int i = n - 1, curturns; i>=0;i--){
            // 0轮是初始
			 curturns = 0;
			 while (r > 0 && stk[r-1][0] < arr[i]){ // 相等直接进栈即可
                curturns = max(curturns + 1, stk[--r][1]);
			 }
			 stk[r][0] = arr[i];
			 stk[r++][1]  = curturns;
			 ans = max(ans, curturns);
		 }
		 return ans;
    }
};
```

## leetcode 1504. 统计全 1 子矩形

[原题](https://leetcode.cn/problems/count-submatrices-with-all-ones/description/)

给你一个 `m x n` 的二进制矩阵 `mat` ，请你返回有多少个 **子矩形** 的元素全部都是 1 。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2021/10/27/ones1-grid.jpg)

```
输入：mat = [[1,0,1],[1,1,0],[1,1,0]]
输出：13
解释：
有 6 个 1x1 的矩形。
有 2 个 1x2 的矩形。
有 3 个 2x1 的矩形。
有 1 个 2x2 的矩形。
有 1 个 3x1 的矩形。
矩形数目总共 = 6 + 2 + 3 + 1 + 1 = 13 。
```

**示例 2：**

[原题配图](https://assets.leetcode.com/uploads/2021/10/27/ones2-grid.jpg)

```
输入：mat = [[0,1,1,0],[0,1,1,1],[1,1,1,0]]
输出：24
解释：
有 8 个 1x1 的子矩形。
有 5 个 1x2 的子矩形。
有 2 个 1x3 的子矩形。
有 4 个 2x1 的子矩形。
有 2 个 2x2 的子矩形。
有 2 个 3x1 的子矩形。
有 1 个 3x2 的子矩形。
矩形数目总共 = 8 + 5 + 2 + 4 + 2 + 2 + 1 = 24 。
```



**提示：**

- `1 <= m, n <= 150`
- `mat[i][j]` 仅包含 `0` 或 `1`

```cpp
class Solution {
public:
    int numSubmat(vector<vector<int>>& mat) {
        //这种子矩阵的问题，特别容易在清算阶段把n和m写反
        int n = mat.size();
        int m = mat[0].size();
        const int maxn = 152;
        int stk[maxn];
        vector<int> arr(m, 0);
        int ans = 0;
        for (int i = 0;i<n;i++){
            int r = 0;
            int cur;
            for (int j = 0; j<m;j++){
                arr[j] = mat[i][j] == 0 ? 0 : arr[j] + 1;//完成直方图
                // 遍历阶段
				while(r > 0 && arr[j] <= arr[stk[r-1]]){
					cur = stk[--r];
					if (arr[j] == arr[cur]){
						continue;
					}
					if (r > 0){
						int left = stk[r-1];
						ans += (j- left - 1) * (j - left) / 2 * (arr[cur] - max(arr[left], arr[j]));
					}
					else{
						int left = -1;
						ans += (j - left - 1) * (j - left) / 2 * (arr[cur] - arr[j]);
					}
				}
				stk[r++] = j;
			}
			// 清算阶段
			while (r > 0){
				cur = stk[--r];
				if (r > 0){
					int left = stk[r-1];
					ans += (m - left - 1) * (m - left) / 2 * (arr[cur] - arr[left]);
				}
				else{
					int left = -1;
					ans += (m - left - 1) * (m - left) / 2 * arr[cur];
				}
			}
		}
		return ans;
    }
};
```
