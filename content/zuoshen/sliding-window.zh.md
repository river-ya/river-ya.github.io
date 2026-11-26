# 滑动窗口

维持左右边界都不回退的一段范围，来求解很多子数组（串）的相关问题

滑动窗口的关键：找到**范围和答案指标**之间的**单调性**关系（类似贪心）

滑动过程：滑动窗口可以用**简单变量或者结构**来维护信息

求解大流程:求子数组在每个位置或结尾情况下的答案（开头还是结尾在于个人习惯）

## [leetcode LCR 008. 长度最小的子数组](https://leetcode.cn/problems/2VG8Kg/)

求>=target的最短子数组长度

给定一个含有 `n` 个正整数的数组和一个正整数 `target` **。**

找出该数组中满足其和 `≥ target` 的长度最小的 **连续子数组** `[numsl, numsl+1, ..., numsr-1, numsr]` ，并返回其长度**。**如果不存在符合条件的子数组，返回 `0` 。



**示例 1：**

```
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：子数组 [4,3] 是该条件下的长度最小的子数组。
```

**示例 2：**

```
输入：target = 4, nums = [1,4,4]
输出：1
```

**示例 3：**

```
输入：target = 11, nums = [1,1,1,1,1,1,1,1]
输出：0
```



提示：

- `1 <= target <= 109`
- `1 <= nums.length <= 105`
- `1 <= nums[i] <= 105`

```cpp
#include <bits/stdc++.h>
using namespace std;
int minsubarraysum(int target, vector<int> & nums){
    int ans = INT_MAX;
    for (int l = 0, r = 0, sum = 0; r < nums.size(); r++){
        sum += nums[r];
        while (sum - nums[l] >= target) sum-= nums[l++];
        //如果l位置的数从窗口出去还能继续达标，那就出去
        if(sum >= target) ans = min(ans, r - l + 1);
    }
    return ans == INT_MAX ? 0 : ans;
}
```

## [leetcode LCR 016. 无重复字符的最长子串](https://leetcode.cn/problems/wtcaE1/description/)

无重复字符的最长子串

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长连续子字符串** 的长度。



**示例 1：**

```
输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子字符串是 "abc"，所以其长度为 3。
```

**示例 2：**

```
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子字符串是 "b"，所以其长度为 1。
```

**示例 3：**

```
输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
```

**示例 4：**

```
输入: s = ""
输出: 0
```



**提示：**

- `0 <= s.length <= 5 * 104`
- `s` 由英文字母、数字、符号和空格组成

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
		int last[256];//每一种字符上次出现的位置
        fill(last, last+256, -1);
		int ans = 0;
		for(int l = 0, r = 0; r<s.size(); r++){
			l = max(last[s[r]] + 1, l);
			ans = max(ans, r - l  + 1);
			last[s[r]] = r;
		}
		return ans;
    }
};
```

## [leetcode LCR 017. 最小覆盖子串](https://leetcode.cn/problems/M1oyTv/description/)

给定两个字符串 `s` 和 `t` 。返回 `s` 中包含 `t` 的所有字符的最短子字符串。如果 `s` 中不存在符合条件的子字符串，则返回空字符串 `""` 。

如果 `s` 中存在多个符合条件的子字符串，返回任意一个。



**注意：** 对于 `t` 中重复字符，我们寻找的子字符串中该字符数量必须不少于 `t` 中该字符数量。



**示例 1：**

```
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最短子字符串 "BANC" 包含了字符串 t 的所有字符 'A'、'B'、'C'
```

**示例 2：**

```
输入：s = "a", t = "a"
输出："a"
```

**示例 3：**

```
输入：s = "a", t = "aa"
输出：""
解释：t 中两个字符 'a' 均应包含在 s 的子串中，因此没有符合条件的子字符串，返回空字符串。
```



**提示：**

- `1 <= s.length, t.length <= 105`
- `s` 和 `t` 由英文字母组成

```cpp
//欠债负债模型
//target ： bccba
//欠债表 cnts ： b: -2, c : -2, a : -1
//总负债 int debt = 5(target.size)
//str : tbtaccb……
//[t] 相当于无效还款
/*
    cnts:
        b: -2, c: -2, a : -1, t : 1;
    debt = 5
*/
//[t b]
// 每种字符的负债情况：
// cnts[i] = 负数，代表字符i有负债
// cnts[i] = 正数，代表字符i有盈余
class Solution {
public:
    string minWindow(string s, string t) {
		int cnts[256];
		fill(cnts, cnts+256, 0);
		int start = 0;
		int len = INT_MAX;
		//debt table
		int debt = t.size();
		for (char ch : t){
			cnts[ch]--;
		}
		for (int l = 0, r = 0; r < s.size(); r++){
			cnts[s[r]]++;
			if (cnts[s[r]] <= 0){
				debt--;
			}
			if (debt == 0){
				while (cnts[s[l]] > 0){
					cnts[s[l++]]--;
				}
				if (r - l + 1 < len){
					len = r - l + 1;
					start = l;
				}
			}
		}
		if (len == INT_MAX) return "";
        return s.substr(start, len);
    }
};
```

## [leetcode 134. 加油站](https://leetcode.cn/problems/gas-station/description/)

在一条环路上有 `n` 个加油站，其中第 `i` 个加油站有汽油 `gas[i]` 升。

你有一辆油箱容量无限的的汽车，从第 `i` 个加油站开往第 `i+1` 个加油站需要消耗汽油 `cost[i]` 升。你从其中的一个加油站出发，开始时油箱为空。

给定两个整数数组 `gas` 和 `cost` ，如果你可以按顺序绕环路行驶一周，则返回出发时加油站的编号，否则返回 `-1` 。如果存在解，则 **保证** 它是 **唯一** 的。



**示例 1:**

```
输入: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
输出: 3
解释:
从 3 号加油站(索引为 3 处)出发，可获得 4 升汽油。此时油箱有 = 0 + 4 = 4 升汽油
开往 4 号加油站，此时油箱有 4 - 1 + 5 = 8 升汽油
开往 0 号加油站，此时油箱有 8 - 2 + 1 = 7 升汽油
开往 1 号加油站，此时油箱有 7 - 3 + 2 = 6 升汽油
开往 2 号加油站，此时油箱有 6 - 4 + 3 = 5 升汽油
开往 3 号加油站，你需要消耗 5 升汽油，正好足够你返回到 3 号加油站。
因此，3 可为起始索引。
```

**示例 2:**

```
输入: gas = [2,3,4], cost = [3,4,3]
输出: -1
解释:
你不能从 0 号或 1 号加油站出发，因为没有足够的汽油可以让你行驶到下一个加油站。
我们从 2 号加油站出发，可以获得 4 升汽油。 此时油箱有 = 0 + 4 = 4 升汽油
开往 0 号加油站，此时油箱有 4 - 3 + 2 = 3 升汽油
开往 1 号加油站，此时油箱有 3 - 3 + 3 = 3 升汽油
你无法返回 2 号加油站，因为返程需要消耗 4 升汽油，但是你的油箱只有 3 升汽油。
因此，无论怎样，你都不可能绕环路行驶一周。
```



**提示:**

- `n == gas.length == cost.length`
- `1 <= n <= 105`
- `0 <= gas[i], cost[i] <= 104`
- 输入保证答案唯一。
