# 一维动态规划

任何一个动态规划问题都一定对应着一个有重复调用行为的递归

但不是任何递归问题都适合改动态规划

斐波那契数列引入

```cpp
//从顶到底的动态规划：记忆化搜索（缓存表）
//时间复杂度O(n)
int dp[maxn] = {-1};
int fib1(int i){
    if (i == 0){
        return 0;
    }
    if (i == 1){
        return 1;
    }
    if (dp[i] != -1){
        return dp[i]; //缓存命中就返回
    }
    int ans = fib1(i-1) + fib1(i-2);
    dp[i] = ans; //挂上缓存
    return ans;
}
//从底到顶的动态规划：严格依赖位置，先算简单位置，再算复杂位置，递推着算
int fib2(int n){
    if (n == 0) return 0;
    if (n == 1) return 1;
    int dp[maxn] = {0};
    dp[1] = 1;
    for (int i = 2; i<n;i++){
        dp[i] = dp[i-1] + dp[i-2];
    }
    return dp[n];
}
//节省空间，用有限变量存
int fib3(int n){
	if (n == 0) return 0;
    if (n == 1) return 1;
    int lastlast = 0, last = 0;
    for (int i = 2, cur; i<n;i++){
        cur = last + lastlast;
        lastlast = last;
        last = cur;
    }
    return cur;
}
```

## leetcode No.983 最低票价

[原题](https://leetcode.cn/problems/minimum-cost-for-tickets/description/)

在一个火车旅行很受欢迎的国度，你提前一年计划了一些火车旅行。在接下来的一年里，你要旅行的日子将以一个名为 `days` 的数组给出。每一项是一个从 `1` 到 `365` 的整数。

火车票有 **三种不同的销售方式** ：

- 一张 **为期一天** 的通行证售价为 `costs[0]` 美元；
- 一张 **为期七天** 的通行证售价为 `costs[1]` 美元；
- 一张 **为期三十天** 的通行证售价为 `costs[2]` 美元。

通行证允许数天无限制的旅行。 例如，如果我们在第 `2` 天获得一张 **为期 7 天** 的通行证，那么我们可以连着旅行 7 天：第 `2` 天、第 `3` 天、第 `4` 天、第 `5` 天、第 `6` 天、第 `7` 天和第 `8` 天。

返回 *你想要完成在给定的列表 `days` 中列出的每一天的旅行所需要的最低消费* 。



**示例 1：**

```
输入：days = [1,4,6,7,8,20], costs = [2,7,15]
输出：11
解释：
例如，这里有一种购买通行证的方法，可以让你完成你的旅行计划：
在第 1 天，你花了 costs[0] = $2 买了一张为期 1 天的通行证，它将在第 1 天生效。
在第 3 天，你花了 costs[1] = $7 买了一张为期 7 天的通行证，它将在第 3, 4, ..., 9 天生效。
在第 20 天，你花了 costs[0] = $2 买了一张为期 1 天的通行证，它将在第 20 天生效。
你总共花了 $11，并完成了你计划的每一天旅行。
```

**示例 2：**

```
输入：days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]
输出：17
解释：
例如，这里有一种购买通行证的方法，可以让你完成你的旅行计划：
在第 1 天，你花了 costs[2] = $15 买了一张为期 30 天的通行证，它将在第 1, 2, ..., 30 天生效。
在第 31 天，你花了 costs[0] = $2 买了一张为期 1 天的通行证，它将在第 31 天生效。
你总共花了 $17，并完成了你计划的每一天旅行。
```



**提示：**

- `1 <= days.length <= 365`
- `1 <= days[i] <= 365`
- `days` 按顺序严格递增
- `costs.length == 3`
- `1 <= costs[i] <= 1000`

```cpp
//暴力递归：超时
class Solution {
public:
    int durations[3] = {1, 7, 30};
    //days[i,…… 旅行最少花费
    int f1(vector<int> & days, vector<int> & costs, int i){
        if (i == days.size()){//后面没有旅行了
            return 0;
        }
        int ans = INT_MAX;
        for (int k = 0, j = i; k<3;k++){
            //k是方案编号：0， 1， 2
            while(j < days.size() && days[i] + durations[k] > days[j]) j++;//找过期票的时间，即下一个开始的旅行时间
            ans = min(ans, costs[k] + f1(days, costs, j));
        }
        return ans;
    }
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        return f1(days, costs, 0);
    }
};
//从顶到底的动态规划：记忆化搜索
class Solution {
public:
    int durations[3] = {1, 7, 30};
    int f2(vector<int> & days, vector<int> & costs, int i, vector<int> & dp){
        if (i == days.size()){
            return 0;
        }
        //存过直接返回该值
        if (dp[i] != -1){
            return dp[i];
        }
        int ans = INT_MAX;
        for (int k = 0, j = i; k<3;k++){
            while(j < days.size() && days[i] + durations[k] > days[j]) j++;
            ans = min(ans, costs[k] + f2(days, costs, j, dp));
        }
        //挂缓存
        dp[i] = ans;
        return ans;
    }
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        vector<int> dp(days.size(), -1);
        return f2(days, costs, 0, dp);
    }
};
//严格位置依赖的动态规划
//从底到顶的动态规划
class Solution {
public:
    int durations[3] = {1, 7, 30};
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        int n = days.size();
        vector<int> dp(days.size() + 1, INT_MAX);
        dp[n] = 0;
        //套用递归的方式
        for (int i = n - 1; i>=0;i--){
            for (int k = 0, j = i; k<3;k++){
                while (j < days.size() && days[i] + durations[k] > days[j]) j++;
                dp[i] = min(dp[i], costs[k] + dp[j]);//暴力递归里怎么尝试的，状态转移方程怎么写
            }
        }
        return dp[0];
    }
};
```

## leetcode No.91 解码方法

[原题](https://leetcode.cn/problems/decode-ways/)

一条包含

```
"1" -> 'A' "2" -> 'B' ... "25" -> 'Y' "26" -> 'Z'
```

然而，在 **解码** 已编码的消息时，你意识到有许多不同的方式来解码，因为有些编码被包含在其它编码当中（`"2"` 和 `"5"` 与 `"25"`）。

例如，`"11106"` 可以映射为：

- `"AAJF"` ，将消息分组为 `(1, 1, 10, 6)`
- `"KJF"` ，将消息分组为 `(11, 10, 6)`
- 消息不能分组为 `(1, 11, 06)` ，因为 `"06"` 不是一个合法编码（只有 "6" 是合法的）。

注意，可能存在无法解码的字符串。

给你一个只含数字的 **非空** 字符串 `s` ，请计算并返回 **解码** 方法的 **总数** 。如果没有合法的方式解码整个字符串，返回 `0`。

题目数据保证答案肯定是一个 **32 位** 的整数。



**示例 1：**

```
输入：s = "12"
输出：2
解释：它可以解码为 "AB"（1 2）或者 "L"（12）。
```

**示例 2：**

```
输入：s = "226"
输出：3
解释：它可以解码为 "BZ" (2 26), "VF" (22 6), 或者 "BBF" (2 2 6) 。
```

**示例 3：**

```
输入：s = "06"
输出：0
解释："06" 无法映射到 "F" ，因为存在前导零（"6" 和 "06" 并不等价）。
```



**提示：**

- `1 <= s.length <= 100`
- `s` 只包含数字，并且可能包含前导零。

```cpp
//从顶到底的记忆化搜索
class Solution {
public:
    int f(string & s, int i, vector<int> & dp){
        if (i == s.size()) return 1;//注意返回1，到底了，说明是一种正确的解码方法，容易写成0
        int ans;
        if (dp[i] != -1){
            return dp[i];
        }
        if (s[i] == '0') ans = 0;//没有解码方案，ans = 0
        else{
            ans = f(s, i+1, dp);
            if ((i+1!=s.size()) && ((s[i] == '1') || (s[i] == '2' && s[i+1] >= '0' && s[i+1] <= '6')) ){
                ans += f(s, i+2, dp);
            }
        }
        dp[i] = ans;
        return ans;
    }
    int numDecodings(string s) {
        int n = s.size();
        vector<int> dp(n+2, -1);
        // dp[n] = 0, dp[n+1] = 0;
        return f(s, 0, dp);
    }
};
//从底到顶的动态规划
//严格位置依赖
class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        vector<int> dp(n+2, -1);
        dp[n] = 1, dp[n+1] = 1;//不用讨论边界
        for (int i = n - 1; i>=0;i--){
            if (s[i] == '0'){
                dp[i] = 0;
                continue;
            }
            dp[i] = dp[i+1];
            if ((i+1 < s.size())&&(s[i] == '1') || (s[i] == '2' && s[i+1] >= '0' && s[i+1] <= '6')){
                dp[i] += dp[i+2];
            }
        }
        return dp[0];
    }
};
//自己写的版本，从底到顶的动态规划
class Solution {
public:
    int check(int x, string s){
        if(s[x] == '1'){
            return 1;
        }
        else if(s[x] <= '2' && s[x+1] <= '6'){
            return 1;
        }
        else {
            return 0;
        }
    }
    int numDecodings(string s) {
        int n = s.size();
        vector<int> dp(n + 1, -1);
        dp[n] = 1;
        dp[n-1] = s[n-1] == '0' ? 0 : 1;
        for (int i = n - 2;i>=0;i--){
            if(s[i] == '0'){
                dp[i] = 0;
            }
            else{
                dp[i] = check(i, s) * dp[i+2] + dp[i+1];
            }
        }
        return dp[0];
    }
};
```

## leetcode No.639 解码方法 II

[原题](https://leetcode.cn/problems/decode-ways-ii/description/)

一条包含字母 `A-Z` 的消息通过以下的方式进行了 **编码** ：

```
'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
```

要 **解码** 一条已编码的消息，所有的数字都必须分组，然后按原来的编码方案反向映射回字母（可能存在多种方式）。例如，`"11106"` 可以映射为：

- `"AAJF"` 对应分组 `(1 1 10 6)`
- `"KJF"` 对应分组 `(11 10 6)`

注意，像 `(1 11 06)` 这样的分组是无效的，因为 `"06"` 不可以映射为 `'F'` ，因为 `"6"` 与 `"06"` 不同。

**除了** 上面描述的数字字母映射方案，编码消息中可能包含 `'*'` 字符，可以表示从 `'1'` 到 `'9'` 的任一数字（不包括 `'0'`）。例如，编码字符串 `"1*"` 可以表示 `"11"`、`"12"`、`"13"`、`"14"`、`"15"`、`"16"`、`"17"`、`"18"` 或 `"19"` 中的任意一条消息。对 `"1*"` 进行解码，相当于解码该字符串可以表示的任何编码消息。

给你一个字符串 `s` ，由数字和 `'*'` 字符组成，返回 **解码** 该字符串的方法 **数目** 。

由于答案数目可能非常大，返回 `109 + 7` 的 **模** 。



**示例 1：**

```
输入：s = "*"
输出：9
解释：这一条编码消息可以表示 "1"、"2"、"3"、"4"、"5"、"6"、"7"、"8" 或 "9" 中的任意一条。
可以分别解码成字符串 "A"、"B"、"C"、"D"、"E"、"F"、"G"、"H" 和 "I" 。
因此，"*" 总共有 9 种解码方法。
```

**示例 2：**

```
输入：s = "1*"
输出：18
解释：这一条编码消息可以表示 "11"、"12"、"13"、"14"、"15"、"16"、"17"、"18" 或 "19" 中的任意一条。
每种消息都可以由 2 种方法解码（例如，"11" 可以解码成 "AA" 或 "K"）。
因此，"1*" 共有 9 * 2 = 18 种解码方法。
```

**示例 3：**

```
输入：s = "2*"
输出：15
解释：这一条编码消息可以表示 "21"、"22"、"23"、"24"、"25"、"26"、"27"、"28" 或 "29" 中的任意一条。
"21"、"22"、"23"、"24"、"25" 和 "26" 由 2 种解码方法，但 "27"、"28" 和 "29" 仅有 1 种解码方法。
因此，"2*" 共有 (6 * 2) + (3 * 1) = 12 + 3 = 15 种解码方法。
```



**提示：**

- `1 <= s.length <= 105`
- `s[i]` 是 `0 - 9` 中的一位数字或字符 `'*'`

```cpp
//从顶到底的记忆化搜索
#define mod 1000000007
using ll = long long;//防溢出
class Solution {
public:
    ll f(string & s, int i, vector<ll> & dp){
        if(i == s.size()) return 1;
        if (s[i] == '0') return 0;
        if (dp[i] != -1){
            return dp[i];
        }
        ll ans = f(s, i+1, dp) * ((s[i] == '*') ? 9 : 1);
        if (i + 1 < s.size()){
            if (s[i] != '*'){
                if (s[i+1] != '*'){
                    if ((s[i] - '0') * 10 + s[i+1] - '0' <= 26){
                        ans += f(s, i+2, dp);
                    }
                }
                else{
                    if (s[i] == '1'){
                        ans += f(s, i+2, dp) * 9;
                    }
                    else if(s[i] == '2'){
                        ans += f(s, i+2, dp) * 6;
                    }
                }

            }
            else{
                if (s[i+1] != '*'){
                    if (s[i+1] >= '0' && s[i+1] <= '6'){
                        ans += f(s, i+2, dp) * 2;
                    }
                    else{
                        ans += f(s, i+2, dp);
                    }
                }
                else{
                    ans += f(s, i+2, dp) * 15;
                }
            }
        }
        ans %= mod;
        dp[i] = ans;
        return ans;
    }
    int numDecodings(string s) {
        vector<ll> dp(s.size()+1, -1);
        return f(s, 0, dp);
    }
};
//从底到顶的动态规划
#define mod 1000000007
using ll = long long;
class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        vector<ll> dp(n+1, -1);
        dp[n] = 1;
        for (int i = n - 1; i>=0;i--){
            if (s[i] == '0'){
                dp[i] = 0;
            }
            else if(s[i] != '*'){
                dp[i] = dp[i+1];
                if (i + 1 <s.size()){
                    if (s[i+1] != '*'){
                        if ((s[i]-'0')* 10 + s[i+1]-'0' <= 26){
                            dp[i] += dp[i+2];
                        }
                    }
                    else{
                        if (s[i] == '1'){
                            dp[i] += dp[i+2] * 9;
                        }
                        if (s[i] == '2'){
                            dp[i] += dp[i+2] * 6;
                        }
                    }
                }
            }
            else{
                dp[i] = 9 * dp[i+1];
                if (i+1 <s.size()){
                    if (s[i+1] != '*'){
                        if (s[i+1] >= '0' && s[i+1] <= '6'){
                            dp[i] += 2 * dp[i+2];
                        }
                        else{
                            dp[i] += dp[i+2];
                        }
                    }
                    else{
                        dp[i] += dp[i+2] * 15;
                    }
                }
            }
            dp[i] %= mod;
        }
        return dp[0];
    }
};
//空间压缩，有限数存储
#define mod 1000000007
using ll = long long;
class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        ll cur = 0, next = 1, nextnext = 0;//dp[i]->cur  dp[i+1]->next, dp[i+2]->nextnext
        for (int i = n - 1; i>=0;i--){
            if (s[i] == '0'){
                cur = 0;
            }
            else if(s[i] != '*'){
                cur = next;
                if (i + 1 <s.size()){
                    if (s[i+1] != '*'){
                        if ((s[i]-'0')* 10 + s[i+1]-'0' <= 26){
                            cur += nextnext;
                        }
                    }
                    else{
                        if (s[i] == '1'){
                            cur += nextnext * 9;
                        }
                        if (s[i] == '2'){
                            cur += nextnext * 6;
                        }
                    }
                }
            }
            else{
                cur = 9 * next;
                if (i+1 <s.size()){
                    if (s[i+1] != '*'){
                        if (s[i+1] >= '0' && s[i+1] <= '6'){
                            cur += 2 * nextnext;
                        }
                        else{
                            cur += nextnext;
                        }
                    }
                    else{
                        cur += nextnext * 15;
                    }
                }
            }
            cur %= mod;
            //丝滑替换
            nextnext = next;
            next = cur;
            cur = 0;
        }
        return next;
    }
};
```

## leetcode No.264 丑数 II

[原题](https://leetcode.cn/problems/ugly-number-ii/)

给你一个整数 `n` ，请你找出并返回第 `n` 个 **丑数** 。

**丑数** 就是质因子只包含 `2`、`3` 和 `5` 的正整数。



**示例 1：**

```
输入：n = 10
输出：12
解释：[1, 2, 3, 4, 5, 6, 8, 9, 10, 12] 是由前 10 个丑数组成的序列。
```

**示例 2：**

```
输入：n = 1
输出：1
解释：1 通常被视为丑数。
```



**提示：**

- `1 <= n <= 1690`

暴力方法

下一项丑数总是前面丑数的2/3/5倍

![课堂推演图 1](/assets/notes/zuoshen/dp-basics-01.jpg)

三指针保证单调性

![课堂推演图 2](/assets/notes/zuoshen/dp-basics-02.jpg)

```cpp
//有一种很好理解的方法：优先队列的方法，但需要unordered_set去重
class Solution {
public:
    int nthUglyNumber(int n) {
        vector<int> factors = {2, 3, 5};
        unordered_set<long long> seen;
        priority_queue<long long, vector<long long>, greater<long long>> pq;
        seen.insert(1);
        pq.push(1);
        long long ugly = 0;
        for (int i = 0;i<n;i++){
            long long cur = pq.top();
            pq.pop();
            ugly = cur;
            for (int factor : factors){
                long long next = cur * factor;
                if (!seen.count(next)){
                    seen.insert(next);
                    pq.push(next);
                }
            }
        }
        return ugly;
    }
};
//最优解
//动态规划+三指针
class Solution {
public:
    int nthUglyNumber(int n) {
        vector<int> dp(n+1, 0);
        dp[1] = 1;
        for (int i = 2, i2 = 1, i3 = 1, i5 = 1, a, b, c, cur; i<=n;i++){
            a = dp[i2] * 2;
            b = dp[i3] * 3;
            c = dp[i5] * 5;
            cur = min(min(a, b), c);
            if (cur == a){
                i2++;
            }
            if (cur == b){
                i3++;
            }
            if (cur == c){
                i5++;
            }//一定不要写else if，因为可能会有公倍数，那么两个指针都要移动
            dp[i] = cur;
        }
        return dp[n];
    }
};
```

## leetcode No32 最长有效括号

[原题](https://leetcode.cn/problems/longest-valid-parentheses/description/)

给你一个只包含 `'('` 和 `')'` 的字符串，找出最长有效（格式正确且连续）括号 子串 的长度。

左右括号匹配，即每个左括号都有对应的右括号将其闭合的字符串是格式正确的，比如 `"(()())"`。



**示例 1：**

```
输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"
```

**示例 2：**

```
输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
```

**示例 3：**

```
输入：s = ""
输出：0
```



**提示：**

- `0 <= s.length <= 3 * 104`
- `s[i]` 为 `'('` 或 `')'`

```cpp
//我写的动态规划
class Solution {
public:
    int longestValidParentheses(string s) {
        int n = s.size();
        vector<int> dp(n, 0);
        for (int i = 1;i<n;i++){
            if (s[i] == '('){
                dp[i] = 0;
                continue;
            }
            int j = i - 1;
            bool flag = true;//是否用过最右边的括号
            while(j>=0){//实际上这个while没有必要，只需要跳一次
                if (s[j] == '(' && flag){
                    j--;
                    flag = false;
                    dp[i] += 2;
                }
                else if (dp[j] != 0){
                    dp[i] += dp[j];
                    j -= dp[j];
                }
                else{
                    break;
                }
            }
            if (flag){
                dp[i] = 0;
            }
        }
        int ans = 0;
        for (int i = 0; i<n;i++){
            ans = max(ans, dp[i]);
        }
        return ans;
    }
};
//左神的动态规划
class Solution {
public:
    int longestValidParentheses(string s) {
        int n = s.size();
        vector<int> dp(n, 0);
        for (int i = 1;i<n;i++){
            if(s[i] != '('){
                int next = i - 1 - dp[i-1];
                if (next >= 0){
                    if (s[next] == ')') dp[i] = 0;
                    else{
                        dp[i] = dp[i-1] + 2 + ((next > 0)?dp[next-1]:0);//只需要跳一次，因为之前连续的都已经连起来了
                    }
                }
            }
        }
        int ans = 0;
        for (int i = 0; i<n;i++){
            ans = max(ans, dp[i]);
        }
        return ans;
    }
};
//后来复习写的版本
class Solution {
public:
    int longestValidParentheses(string s) {
        if(s.size() <= 1) return 0;
        int n = s.size();
        vector<int> dp(n+1, 0);
        for(int i = n-2;i>=0;i--){
            if(s[i] == '('){
                int next = dp[i+1] + i + 1;
				if (next < s.size() && s[next] == ')' ){
					dp[i] = dp[next + 1] + 2 + dp[i+1];
				}
			}
		}
        int ans = INT_MIN;
        for (int i = 0;i<n;i++){
            ans = max(ans, dp[i]);
        }
		return ans;
    }
};
```

## leetcode No.467 环绕字符串中唯一的子字符串

[原题](https://leetcode.cn/problems/unique-substrings-in-wraparound-string/)

定义字符串 `base` 为一个 `"abcdefghijklmnopqrstuvwxyz"` 无限环绕的字符串，所以 `base` 看起来是这样的：

- `"...zabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd...."`.

给你一个字符串 `s` ，请你统计并返回 `s` 中有多少 **不同** **非空子串** 也在 `base` 中出现。



**示例 1：**

```
输入：s = "a"
输出：1
解释：字符串 s 的子字符串 "a" 在 base 中出现。
```

**示例 2：**

```
输入：s = "cac"
输出：2
解释：字符串 s 有两个子字符串 ("a", "c") 在 base 中出现。
```

**示例 3：**

```
输入：s = "zab"
输出：6
解释：字符串 s 有六个子字符串 ("z", "a", "b", "za", "ab", and "zab") 在 base 中出现。
```



**提示：**

- `1 <= s.length <= 105`
- s 由小写英文字母组成

![课堂推演图 3](/assets/notes/zuoshen/dp-basics-03.jpg)

```cpp
//超时版，重复计算了很多子串
class Solution {
public:
    int findSubstringInWraproundString(string s) {
        int dp[26] = {0};
        int n = s.size();
        for (int i = 0; i<n;i++){
            int j = 1;
            for (; i + j < n && ((s[i+j-1] == 'z' && s[i+j] == 'a' )|| s[i+j] - s[i+j-1] == 1); j++);
            dp[s[i] - 'a'] = max(dp[s[i] - 'a'], j);
		}
		int ans = 0;
		for(int i = 0;i<26;i++){
			ans += dp[i];
		}
		return ans;
    }
};
//计算以不同字母结尾的最长子串长度，然后把各个长度相加即为最终答案
//利用len避免重复计算子串，表示当前最长连续有效数字
class Solution {
public:
    int findSubstringInWraproundString(string s) {
        int n = s.size();
        int dp[26] = {0};//dp数组只跟字符种类有关，不是位置依赖
        int len = 1;
        dp[s[0] - 'a'] = 1;
        for(int i = 1; i < n;i++){
            if ((s[i] - s[i-1] == 1 )|| (s[i] == 'a' && s[i-1] == 'z')){
                len++;
            }
            else{
                len = 1;
            }
            dp[s[i] - 'a'] = max(dp[s[i] - 'a'], len);
        }
        int sum = 0;
        for (int i = 0; i<26;i++){
            sum += dp[i];
        }
        return sum;
    }
};
```

## leetcode No.940 不同的子序列 II

[原题](https://leetcode.cn/problems/distinct-subsequences-ii/)

给定一个字符串 `s`，计算 `s` 的 **不同非空子序列** 的个数。因为结果可能很大，所以返回答案需要对 **`10^9 + 7` 取余** 。

字符串的 **子序列** 是经由原字符串删除一些（也可能不删除）字符但不改变剩余字符相对位置的一个新字符串。

- 例如，`"ace"` 是 `"***a***b***c***d***e***"` 的一个子序列，但 `"aec"` 不是。



**示例 1：**

```
输入：s = "abc"
输出：7
解释：7 个不同的子序列分别是 "a", "b", "c", "ab", "ac", "bc", 以及 "abc"。
```

**示例 2：**

```
输入：s = "aba"
输出：6
解释：6 个不同的子序列分别是 "a", "b", "ab", "ba", "aa" 以及 "aba"。
```

**示例 3：**

```
输入：s = "aaa"
输出：3
解释：3 个不同的子序列分别是 "a", "aa" 以及 "aaa"。
```



**提示：**

- `1 <= s.length <= 2000`
- `s` 仅由小写英文字母组成

 之前的字符列都要保留（老的），当前位置的字符加到之前的每个子集里面（纯新增=all - 当前字符上次记录）

实际上可以理解为，纯新的就是先把老的all都保留下来，上次加的同样字符记录此次会同样出现，需要减去

![课堂推演图 4](/assets/notes/zuoshen/dp-basics-04.jpg)

之前有以a结尾的，现在再往前推会再算一次以a结尾，所以需要减去当前字符上次记录的

```cpp
#define mod 1000000007
using ll = long long;
class Solution {
public:
    int distinctSubseqII(string s) {
        int n = s.size();
        ll all = 1;//这个虚拟空集很重要，一开始就算上，最后再减去
        ll dp[26] = {0};//有多少个子序列是以某个字符结尾的
        for (int i = 0; i<n;i++){
            ll new_num = (all - dp[s[i] - 'a'] + mod) % mod;
            all =(new_num + all) % mod;
            dp[s[i] - 'a'] = (dp[s[i] - 'a'] + new_num) % mod;//核心公式
        }
        return (all-1 + mod) % mod ;
    }
};
```

## 一维动态规划总结

动态规划的大致过程：

尝试顺序可能有多种（从头到尾/从尾到头，按喜好来，不过有的题目会有限制）

1. 记忆化搜索（从顶到底的动态规划），**如果每个状态的计算枚举代价很低，往往到这里就可以了**
2. 严格位置依赖的动态规划（从底到顶的动态规划），更多是为了下面说的 **进一步优化枚举做的准备**（简单->复杂）
3. 进一步优化空间（**空间压缩**），一维、二维、多维动态规划都存在这种优化
4. **进一步优化枚举也就是优化时间**

解决一个问题可能有很多尝试方法：

众多的尝试方法中，可能有若干的尝试方法有重复调用的情况，可以转化成动态规划

若干个可以转化成动态规划的方法中，又可能有优劣之分

判定哪个是最优的动态规划方法，**依据题目具体参数的数据量**

最优的动态规划方法实现后，后续又有一整套的优化技巧

# 从递归入手二维动态规划

尝试函数有1个可变参数可以**完全决定返回值**，进而可以改出1维动态规划表的实现

尝试函数有2个可变参数可以**完全决定返回值**，进而可以改出2维动态规划表的实现

## leetcode LCR 099. 最小路径和

[原题](https://leetcode.cn/problems/0i0mDW/)

给定一个包含非负整数的 `*m* x *n*` 网格 `grid` ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

**说明：**一个机器人每次只能向下或者向右移动一步。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2020/11/05/minpath.jpg)

```
输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。
```

**示例 2：**

```
输入：grid = [[1,2,3],[4,5,6]]
输出：12
```



**提示：**

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 200`
- `0 <= grid[i][j] <= 100`
```cpp
//超时递归版本
class Solution {
public:
	int f1(vector<vector<int>> & grid, int i, int j){
		if (i == 0 && j == 0) return grid[i][j];
		int up = INT_MAX;
		int left = INT_MAX;
		if(i - 1 >= 0){
			up = f1(grid, i - 1, j);
		}
		if(j - 1 >= 0){
			left = f1(grid, i, j - 1);
		}
		return grid[i][j] + min(up, left);
	}
    int minPathSum(vector<vector<int>>& grid) {
		return f1(grid, grid.size() - 1, grid[0].size() - 1);
    }
};
//记忆化搜索版本，就是加了个二维表格缓存
class Solution {
public:
	int f2(vector<vector<int>> & grid, int i, int j, vector<vector<int>> & dp){
		if(dp[i][j] != -1){
			return dp[i][j];//缓存命中
		}
		int ans = 0;
		if (i == 0 && j == 0) ans = grid[0][0];
		else{
			int up = INT_MAX;
			int left = INT_MAX;
			if(i - 1 >= 0){
				up = f2(grid, i - 1, j, dp);
			}
			if(j - 1 >= 0){
				left = f2(grid, i, j - 1, dp);
			}
			ans = grid[i][j] + min(up, left);
		}
		dp[i][j] = ans;//挂缓存
		return ans;
	}
    int minPathSum(vector<vector<int>>& grid) {
        int n = grid.size();
        int m = grid[0].size();
        vector<vector<int>> dp(n, vector<int>(m, -1));
		return f2(grid, grid.size() - 1, grid[0].size() - 1, dp);
    }
};
//严格的位置依赖
class Solution {
public:
	int minPathSum(vector<vector<int>>& grid) {
        int n = grid.size();
        int m = grid[0].size();
        vector<vector<int>> dp(n, vector<int> (m, -1));
		dp[0][0] = grid[0][0];
		for(int i = 1;i<n;i++){
			dp[i][0] = dp[i-1][0] + grid[i][0];
		}
		for (int j = 1;j<m;j++){
			dp[0][j] = dp[0][j-1] + grid[0][j];
		}
		for (int i = 1; i<n;i++){
			for (int j = 1; j<m;j++){
				dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j];
			}
		}
		return dp[n-1][m-1];
    }
};
//空间压缩
class Solution {
public:
	int minPathSum(vector<vector<int>>& grid) {
        int n = grid.size();
        int m = grid[0].size();
        vector<int> dp(m, -1);
		dp[0] = grid[0][0];
		for (int j = 1;j<m;j++){
			dp[j] = dp[j-1] + grid[0][j];
		}
		for (int i = 1; i<n;i++){
			for (int j = 0; j<m;j++){
                if(j == 0){
                    dp[j] += grid[i][j];
                }
                else{
                    dp[j] = min(dp[j-1], dp[j]) + grid[i][j];
                }
			}
		}
		return dp[m-1];
    }
};
```

动态规划表的大小：**每个可变参数的可能性数量相乘**

动态规划方法的时间复杂度：**动态规划表的大小 * 每个格子的枚举代价**

二维动态规划依然需要整理**动态规划表的格子之间的依赖关系**

找寻依赖关系，往往通过**画图来建立空间感**，使其显而易见

依然是 **从简单格子填写到复杂格子**的过程，即**严格位置依赖的动态规划**（从底到顶）

## leetcode 79. 单词搜索

[原题](https://leetcode.cn/problems/word-search/)

给定一个 `m x n` 二维字符网格 `board` 和一个字符串单词 `word` 。如果 `word` 存在于网格中，返回 `true` ；否则，返回 `false` 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2020/11/04/word2.jpg)

```
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCCED"
输出：true
```

**示例 2：**

[原题配图](https://assets.leetcode.com/uploads/2020/11/04/word-1.jpg)

```
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "SEE"
输出：true
```

**示例 3：**

[原题配图](https://assets.leetcode.com/uploads/2020/10/15/word3.jpg)

```
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCB"
输出：false
```



**提示：**

- `m == board.length`
- `n = board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` 和 `word` 仅由大小写英文字母组成

```cpp
class Solution {
public:
	bool f(vector<vector<char>> & board, string word, int i, int j, int k){
		if (k == word.size()){
			return true;
		}
		if (i < 0 || i == board.size() || j < 0 || j == board[0].size() || board[i][j] != word[k]){
			return false;
		}
		char tmp = board[i][j];
		board[i][j] = 0;//ascII
		bool ans = f(board, word, i - 1, j, k+1) || f(board, word, i, j - 1, k+1) || f(board, word, i+1, j, k+1) || f(board, word, i, j+1, k+1);
		board[i][j] = tmp;//恢复现场
		return ans;
	}
    bool exist(vector<vector<char>>& board, string word) {
        int n = board.size();
		int m = board[0].size();
		bool flag = false;
		for (int i = 0; i<n;i++){
			for(int j = 0;j<m;j++){
				flag = f(board, word, i, j, 0);
				if (flag){
					return flag;
				}
			}
		}
		return false;
    }
};
```

尝试改动态规划：

只有i，j，k三个参数吗？

并不是，过程中修改了grid的值（恢复现场之前），并不只有三个参数

**带路径的递归（可变参数类型复杂），不适合或者说没有必要改成动态规划的必要**

看题目条件

- `1 <= m, n <= 6`
- `1 <= word.length <= 15`

也反映出只有小数据量，可以直接dfs+恢复现场暴搜

能改成动态规划的递归，统一特征：

**决定返回值的可变参数类型往往都比较简单，一般不会比int类型更复杂**

## leetcode LCR 095. 最长公共子序列

[原题](https://leetcode.cn/problems/qJnOS7/description/)

给定两个字符串 `text1` 和 `text2`，返回这两个字符串的最长 **公共子序列** 的长度。如果不存在 **公共子序列** ，返回 `0` 。

一个字符串的 **子序列** 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

- 例如，`"ace"` 是 `"abcde"` 的子序列，但 `"aec"` 不是 `"abcde"` 的子序列。

两个字符串的 **公共子序列** 是这两个字符串所共同拥有的子序列。



**示例 1：**

```
输入：text1 = "abcde", text2 = "ace"
输出：3
解释：最长公共子序列是 "ace" ，它的长度为 3 。
```

**示例 2：**

```
输入：text1 = "abc", text2 = "abc"
输出：3
解释：最长公共子序列是 "abc" ，它的长度为 3 。
```

**示例 3：**

```
输入：text1 = "abc", text2 = "def"
输出：0
解释：两个字符串没有公共子序列，返回 0 。
```



**提示：**

- `1 <= text1.length, text2.length <= 1000`
- `text1` 和 `text2` 仅由小写英文字符组成。

不管是几维的动态规划

经常**从递归的定义出发，避免后续进行很多边界讨论**

```cpp
//暴力解法，会超时
class Solution {
public:
	// s1[0 ……i1] s2[0 ……i2] 最长公共子序列
	int f1(string s1, string s2, int i1, int i2){
		if (i1 < 0 || i2 < 0) return 0;//i1和i2可能到0以下 ，下标越界很麻烦
		int p1 = f1(s1, s2, i1-1, i2-1);
		int p2 = f1(s1, s2, i1-1, i2);
		int p3 = f1(s1, s2, i1, i2-1);
		int p4 = s1[i1] == s2[i2] ? (p1 + 1) : 0;
		return max(max(p1, p2), max(p3, p4));
	}
    int longestCommonSubsequence(string text1, string text2) {
		int n = text1.size();
		int m = text2.size();
		return f1(text1, text2, n-1, m-1);
    }
};
class Solution {
public:
	// s1[前缀长度为len1] 对应s2[前缀长度为len2] 最长公共子序列
	int f2(string s1, string s2, int len1, int len2){
		if (len1 == 0 || len2 == 0) return 0;
		int ans;
		//如果最后i1和i2相等，那么不需要再考虑p2和p3了，p4直接结算一定更优
		if(s1[len1 - 1] == s2[len2 - 1]){
			ans = f2(s1, s2, len1 - 1, len2 - 1) + 1;
		}
		else{
            //利用单调性p1一定比p2和p3差，因为后者的范围更大
			ans = max(f2(s1, s2, len1 - 1, len2), f2(s1, s2, len1, len2 - 1));
		}
		return ans;
	}
    int longestCommonSubsequence(string text1, string text2) {
		int n = text1.size();
		int m = text2.size();
		return f2(text1, text2, n, m);
    }
};
cpp
//记忆化搜索
class Solution {
public:
	// s1[前缀长度为len1] 对应s2[前缀长度为len2] 最长公共子序列
	int f2(string s1, string s2, int len1, int len2, vector<vector<int>> & dp){
		if (dp[len1][len2] != -1){
			return dp[len1][len2];
		}
		if (len1 == 0 || len2 == 0) return 0;
		int ans;
		//利用单调性p1一定比p2和p3差，因为后者的范围更大
		//如果最后i1和i2相等，那么不需要再考虑p2和p3了，p4直接结算一定更优
		if(s1[len1 - 1] == s2[len2 - 1]){
			ans = f2(s1, s2, len1 - 1, len2 - 1, dp) + 1;
		}
		else{
			ans = max(f2(s1, s2, len1 - 1, len2, dp), f2(s1, s2, len1, len2 - 1, dp));
		}
		dp[len1][len2] = ans;
		return ans;
	}
    int longestCommonSubsequence(string text1, string text2) {
		int n = text1.size();
		int m = text2.size();
		vector<vector<int>> dp(n+1, vector<int> (m+1, -1));//注意dp的大小
		return f2(text1, text2, n, m, dp);
    }
};
cpp
//严格位置依赖
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
		int n = text1.size();
		int m = text2.size();
		vector<vector<int>> dp(n+1, vector<int> (m+1, 0));//注意dp的大小
		//第0行和第0列全为0，因为其中一个序列没有长度
		for(int len1 = 1; len1 <= n; len1++){
			for (int len2 = 1; len2 <= m; len2++){//所有剩余格子都有左上，左，上
				if (text1[len1 - 1] == text2[len2 - 1]){
					dp[len1][len2] = 1 + dp[len1-1][len2-1];
				}
				else{
					dp[len1][len2] = max(dp[len1-1][len2], dp[len1][len2-1]);
				}
			}
		}
		return dp[n][m];
    }
};
//空间压缩
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        string s1, s2;
        //较长的准备为s1，较短的准备为s2，s2是将来的列，一维数组尽量的短
		if(text1.size() >= text2.size()){
			s1 = text1;
			s2 = text2;
		}
		else{
			s1 = text2;
			s2 = text1;
		}
		int n = s1.size();
		int m = s2.size();
		vector<int> dp(m+1, 0);
		//用dp[0]跟着滚动下去
		for(int len1 = 1; len1 <= n; len1++){
			for (int len2 = 1; len2 <= m; len2++){
                int tmp = dp[len2];
				if (s1[len1-1] == s2[len2-1]){
					dp[len2] = dp[0] + 1;
				}
				else{
					dp[len2] = max(dp[len2 - 1], dp[len2]);
				}
                dp[0] = tmp;
			}
            dp[0] = 0;
		}
		return dp[m];
    }
};
```

## leetcode 516. 最长回文子序列

[原题](https://leetcode.cn/problems/longest-palindromic-subsequence/description/)

给你一个字符串 `s` ，找出其中最长的回文子序列，并返回该序列的长度。

子序列定义为：不改变剩余字符顺序的情况下，删除某些字符或者不删除任何字符形成的一个序列。



**示例 1：**

```
输入：s = "bbbab"
输出：4
解释：一个可能的最长回文子序列为 "bbbb" 。
```

**示例 2：**

```
输入：s = "cbbd"
输出：2
解释：一个可能的最长回文子序列为 "bb" 。
```



**提示：**

- `1 <= s.length <= 1000`
- `s` 仅由小写英文字母组成

```cpp
//翻转字符串后和lcs同一个题
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        string s1 = s;
		string s2(s.rbegin(), s.rend());
		int n = s.size();
		vector<int> dp(n+1, 0);
		for (int i = 1; i <= n; i++){
			for (int j = 1; j <= n; j++){
				int tmp = dp[j];
				if (s1[i-1] == s2[j-1]){
					dp[j] = dp[0] + 1;
				}
				else{
					dp[j] = max(dp[j-1], dp[j]);
				}
				dp[0] = tmp;
			}
			dp[0] = 0;
		}
		return dp[n];
    }
};
//有点像区间dp
//暴力方法
class Solution {
public:
	// s[l ……r]最长回文子序列长度 ，区间dp往往是首尾尝试
	int f1(string  & s, int l, int r){
		if (l == r) return 1; //长度为1的首尾长度回文子序列长度是1
		if (l + 1 == r) return (s[l] == s[r] ? 2 : 1);
		if (s[l] == s[r]){
			return 2 + f1(s, l+1, r-1);
		}
		else{
			return max(f1(s, l+1, r), f1(s, l, r-1));
		}
	}
    int longestPalindromeSubseq(string s) {
        int n = s.size();
		return f1(s, 0, n-1);
    }
};
//记忆化搜索
class Solution {
public:
	// s[l ……r]最长回文子序列长度 ，区间dp往往是首尾尝试
	int f1(string  & s, int l, int r, vector<vector<int>> & dp){
		if (dp[l][r] != -1){
			return dp[l][r];
		}
		int ans;
		if (l == r) ans = 1; //长度为1的首尾长度回文子序列长度是1
		else if (l + 1 == r) ans = (s[l] == s[r] ? 2 : 1);
		else{
			if (s[l] == s[r]){
				ans = 2 + f1(s, l+1, r-1, dp);
			}
			else{
				ans = max(f1(s, l+1, r, dp), f1(s, l, r-1, dp));
		}
		}
		dp[l][r] = ans;
		return ans;
	}
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        //考虑l和r的范围来确定dp表的大小
        vector<vector<int>> dp(n, vector<int> (n, -1));
		return f1(s, 0, n-1,dp);
    }
};
//严格位置依赖
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        //考虑l和r的范围来确定dp表的大小
        vector<vector<int>> dp(n, vector<int> (n, -1));
        //画二维格子判断依赖关系。左下，左，下，一开始可以把对角线和对角线向右上挪动一格的填充好，此时有两种填充方式：
		//从下往上从左往右
		//对角线填充
		for(int i = 0; i < n; i++){
			dp[i][i] = 1;
			if (i != n-1){
				dp[i][i+1] = s[i] == s[i+1] ? 2 : 1;
			}
		}
		for (int i = n - 3; i >= 0; i--){
			for (int j = i + 2; j < n; j++){
				if(s[i] == s[j]){
					dp[i][j] = dp[i+1][j-1] + 2;
				}
				else{
					dp[i][j] = max(dp[i+1][j], dp[i][j-1]);
				}
			}
		}

		return dp[0][n-1];
    }
};
//只用一次循环写法
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        //考虑l和r的范围来确定dp表的大小
        vector<vector<int>> dp(n, vector<int> (n, -1));
        //画二维格子判断依赖关系。左下，左，下，一开始可以把对角线和对角线向右上挪动一格的填充好，此时有两种填充方式：
		//从下往上从左往右
		//对角线填充
		for (int l = n - 1; l>=0; l--){
			dp[l][l] = 1;
			if (l + 1 < n){
				dp[l][l+1] = s[l] == s[l+1] ? 2 : 1;
			}
			for (int r = l + 2; r < n; r++){
				if (s[l] == s[r]){
					dp[l][r] = dp[l+1][r-1] +2;
				}
				else{
					dp[l][r] = max(dp[l+1][r], dp[l][r-1]);
				}
			}
		}
		return dp[0][n-1];
    }
};
//空间压缩
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        vector<int> dp(n, 0);
        int leftdown, tmp;
        for (int l = n - 1; l>= 0; l--){
            dp[l] = 1;
            if (l + 1 < n){
                leftdown = dp[l+1];
                dp[l+1] = s[l] == s[l+1] ? 2 : 1;
			}
            for (int r = l + 2; r < n; r++){
                tmp = dp[r];
                if (s[r] == s[l]){
                    dp[r] = leftdown + 2;
				}else{
					dp[r] = max(dp[r], dp[r-1]);
				}
				leftdown = tmp;
			}
		}
		return dp[n-1];
    }
};
```

## nowcode 二叉树

[原题](https://www.nowcoder.com/questionTerminal/aaefe5896cce4204b276e213e725f3ea)

小强现在有n个节点,他想请你帮他计算出有多少种不同的二叉树满足节点个数为n且树的高度不超过m的方案.因为答案很大,所以答案需要模上1e9+7后输出.
 树的高度: 定义为所有叶子到根路径上节点个数的最大值.

链接：https://www.nowcoder.com/questionTerminal/aaefe5896cce4204b276e213e725f3ea
来源：牛客网



数据范围：1≤n,m≤50

  进阶：时间复杂度O(mn^2)，空间复杂度O(nm)


##### **输入描述:**

```
第一行输入两个正整数nnn和mmm.
1≤m≤n≤50
```

##### **输出描述:**

```
输出一个答案表示方案数
cpp
//记忆化搜索
#include<bits/stdc++.h>
using namespace std;
#define mod 1000000007
using ll = long long;
int n, m;
ll f1(int num, int height, vector<vector<ll>> & dp){
	ll ans = 0;
	//空树算一种结构
    if (num == 0) return 1;
	if (height == 0) return 0;
	if (dp[num][height] != -1) return dp[num][height];
    //一共num个节点，头占掉一个节点，左树占用i个，[0, n - 1],右树占用n - i - 1个
	for (int i = 0; i < num; i++){
		ans = (ans + (f1(i, height - 1, dp) * f1(num - 1 - i, height - 1, dp)) % mod) % mod;
	}
	dp[num][height] = ans % mod;
	return ans % mod;
}
int main(){
	cin >> n >> m;
	//节点数为n，高度不超过m
	//两个严格限制条件
	//二维动态规划
	vector<vector<ll>> dp(n + 1, vector<ll>(m + 1, -1));
	cout <<  f1(n, m, dp);
}
//严格位置依赖
#include<bits/stdc++.h>
using namespace std;
#define mod 1000000007
using ll = long long;
int n, m;
int main(){
	cin >> n >> m;
	//节点数为n，高度不超过m
	//两个严格限制条件
	//二维动态规划
	vector<vector<ll>> dp(n + 1, vector<ll>(m + 1, 0));
	for (int height = 0; height <= m; height++){
		dp[0][height] = 1;
	}
	for (int num = 1; num <= n; num++){
		dp[num][0] = 0;
	}
	//依赖关系：左上一长条
	//从上到下，从左往右
	for (int height = 1; height <= m; height++){
		for (int num = 1; num <= n; num++){
			for (int k = 0; k < num; k++){
				dp[num][height] = (dp[num][height] + (dp[k][height-1] * dp[num-k-1][height-1]) % mod) % mod;
			}
		}
	}
	cout << dp[n][m];
}
//空间压缩
#include<bits/stdc++.h>
using namespace std;
#define mod 1000000007
using ll = long long;
int n, m;
int main(){
	cin >> n >> m;
	//节点数为n，高度不超过m
	//两个严格限制条件
	//二维动态规划
	vector<ll> dp1(n + 1, 0);
	vector<ll> dp2(n + 1, 0);
	dp1[0] = 1;
	dp2[0] = 1;
	for (int col = 1; col <= m; col++){
		for (int num = 1; num <= n; num++){
			for (int k = 0; k < num; k++){
				dp2[num] = (dp2[num] + (dp1[k] * dp1[num - k - 1]) % mod) % mod;
			}
		}
		for (int i = 1; i<=n;i++){
			dp1[i] = dp2[i];
			dp2[i] = 0;
		}
	}
	cout << dp1[n];
}
```

## leetcode LCR 112. 矩阵中的最长递增路径 ）

[原题](https://leetcode.cn/problems/fpTFWP/)

给定一个 `m x n` 整数矩阵 `matrix` ，找出其中 **最长递增路径** 的长度。

对于每个单元格，你可以往上，下，左，右四个方向移动。 **不能** 在 **对角线** 方向上移动或移动到 **边界外**（即不允许环绕）。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2021/01/05/grid1.jpg)

```
输入：matrix = [[9,9,4],[6,6,8],[2,1,1]]
输出：4
解释：最长递增路径为 [1, 2, 6, 9]。
```

**示例 2：**

[原题配图](https://assets.leetcode.com/uploads/2021/01/27/tmp-grid.jpg)

```
输入：matrix = [[3,4,5],[3,2,6],[2,2,1]]
输出：4
解释：最长递增路径是 [3, 4, 5, 6]。注意不允许在对角线方向上移动。
```

**示例 3：**

```
输入：matrix = [[1]]
输出：1
```



**提示：**

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 200`
- `0 <= matrix[i][j] <= 231 - 1`

```cpp
//单调关系不用考虑回头路的问题
//数值比你大的格子本身dp表的数据是死的，不会变化
//严格位置依赖没法写，不知道怎么遍历
class Solution {
public:
	int f(vector<vector<int>> & matrix, int i, int j, vector<vector<int>> & dp){
		if (dp[i][j] != 0) return dp[i][j];
		int next = 0;
		int n = matrix.size();
		int m = matrix[0].size();
		if (i > 0 && matrix[i][j] < matrix[i-1][j]){
			next = max(next, f(matrix, i-1, j, dp));
		}
		if (i < n - 1 && matrix[i][j] < matrix[i+1][j]){
			next = max(next, f(matrix, i+1, j, dp));
		}
		if (j > 0 && matrix[i][j] < matrix[i][j-1]){
			next = max(next, f(matrix, i, j-1, dp));
		}
		if (j < m - 1 && matrix[i][j] < matrix[i][j+1]){
			next = max(next, f(matrix, i, j+1, dp));
		}
		dp[i][j] = next + 1;
		return next + 1;
	}
    int longestIncreasingPath(vector<vector<int>>& matrix) {
		int n = matrix.size();
		int m = matrix[0].size();
		vector<vector<int>> dp(n, vector<int> (m, 0));
		int ans = 0;
		for (int i = 0; i<n;i++){
			for (int j = 0; j<m;j++){
				ans = max(ans, f(matrix, i, j, dp));
			}
		}
		return ans;
    }
};
```

# 直接分析二维动态规划

## leetcode LCR 097. 不同的子序列

[原题](https://leetcode.cn/problems/21dk04/description/)

给定一个字符串 `s` 和一个字符串 `t` ，计算在 `s` 的子序列中 `t` 出现的个数。

字符串的一个 **子序列** 是指，通过删除一些（也可以不删除）字符且不干扰剩余字符相对位置所组成的新字符串。（例如，`"ACE"` 是 `"ABCDE"` 的一个子序列，而 `"AEC"` 不是）

题目数据保证答案符合 32 位带符号整数范围。



**示例 1：**

```
输入：s = "rabbbit", t = "rabbit"
输出：3
解释：
如下图所示, 有 3 种可以从 s 中得到 "rabbit" 的方案。
rabbbit
rabbbit
rabbbit
```

**示例 2：**

```
输入：s = "babgbag", t = "bag"
输出：5
解释：
如下图所示, 有 5 种可以从 s 中得到 "bag" 的方案。
babgbag
babgbag
babgbag
babgbag
babgbag
```



**提示：**

- `0 <= s.length, t.length <= 1000`
- `s` 和 `t` 由英文字母组成

```cpp
using ll = unsigned long long;
class Solution {
public:
    int numDistinct(string s, string t) {
		int n = s.size();
		int m = t.size();
		vector<vector<ll>> dp(n+1, vector<ll> (m+1, 0));
		// dp[i][j] ： s[0 ……i - 1] 的子序列对应多少个t[0……j - 1]子串 ,i和j表示长度
        //s[前缀长度为i]的所有子序列中，有多少个子序列等于t[前缀长度为j]
		//从左往右，从上到下
		//对于i-1位置的数：
		//要？需要满足条件：s[i-1] = t[j-1]
		//dp[i][j] += dp[i-1][j-1]
		//不要？
		//dp[i][j] += dp[i-1][j]
        //也就是说如果满足条件需要加两项，不满足条件只加一项
        for(int i = 0; i<=n;i++){
            dp[i][0] = 1;//空串算1
        }
		for (int i = 1; i<=n;i++){
			for (int j = 1; j<=m;j++){
				dp[i][j] += dp[i-1][j];
				if (s[i-1] == t[j-1]){
					dp[i][j] += dp[i-1][j-1];
				}
			}
		}
		return dp[n][m];
    }
};
//空间压缩
using ll = unsigned long long;
class Solution {
public:
    int numDistinct(string s, string t) {
		int n = s.size();
		int m = t.size();
		vector<ll> dp(m + 1, 0);
		dp[0] = 1;
		for (int i = 1; i<=n;i++){
			for (int j = m; j>=1;j--){
                //注意必须是从右往左填，因为如果从左往右填会导致把更新的值当成上一行的左上
				if (s[i-1] == t[j-1]){
					dp[j] += dp[j-1];
				}
			}
		}
		return dp[m];
    }
};
```

## leetcode 72. 编辑距离

[原题](https://leetcode.cn/problems/edit-distance/description/)

给你两个单词 `word1` 和 `word2`， *请返回将 `word1` 转换成 `word2` 所使用的最少操作数* 。

你可以对一个单词进行如下三种操作：

- 插入一个字符
- 删除一个字符
- 替换一个字符

 (编辑距离的一种特例，加权入参按照1：1：1)

**示例 1：**

```
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

**示例 2：**

```
输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')
```



**提示：**

- `0 <= word1.length, word2.length <= 500`
- `word1` 和 `word2` 由小写英文字母组成

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int n = word1.size();
        int m = word2.size();
        vector<vector<int>> dp(n+1, vector<int> (m+1, 0));
        int a = 1, b = 1, c = 1;
		//dp[i][j] : s1[0 ……i-1]，s2[0……j-1]
		// insert_cost = a, del_cost = b, replace_cost = c
		/*
		1. s1[i-1]参与
			a) s1[i-1] 变成 s2[j-1]
                (1) s1[i-1] == s2[j-1], 没有代价，转化为 dp[i-1][j-1]
                (2) s1[i-1] != s2[i-1], 代价为c， 转化为 dp[i-1][j-1] + c
			b) s1[i-1] 不变成s2[j-1], 考虑s2[j-2]位置，最后再插入s2[j-1], 代价为a, 转化为dp[i][j-1] + a
		2. s1[i-1]不参与 删除s1[i-1]，代价为b, 转化为 dp[i-1][j] + b
		*/
		for (int i = 0; i<=m;i++){
			dp[0][i] = i * a;
		}
		for (int i = 0; i<=n;i++){
			dp[i][0] = i * b;
		}
		for (int i = 1; i <= n;i++){
			for (int j = 1; j<=m;j++){
				dp[i][j] = min(min(dp[i-1][j-1] + (word1[i-1] != word2[j-1] ? c : 0), dp[i][j-1] + a), dp[i-1][j] + b);
			}
		}
		return dp[n][m];
    }
};
//小优化
class Solution {
public:
    int minDistance(string word1, string word2) {
        int n = word1.size();
        int m = word2.size();
        vector<vector<int>> dp(n+1, vector<int> (m+1, 0));
        int a = 1, b = 1, c = 1;
		//dp[i][j] : s1[0 ……i-1]，s2[0……j-1]
		// insert_cost = a, del_cost = b, replace_cost = c
		/*
        3. 优化：如果s1[i-1] == s2[j-1]
        那么dp[i-1][j-1]一定最优
		*/
		for (int i = 0; i<=m;i++){
			dp[0][i] = i * a;
		}
		for (int i = 0; i<=n;i++){
			dp[i][0] = i * b;
		}
		for (int i = 1; i <= n;i++){
			for (int j = 1; j<=m;j++){
				if(word1[i-1] == word2[j-1]){
					dp[i][j] = dp[i-1][j-1];
				}
				else{
					dp[i][j] = min(min(dp[i-1][j-1] + c, dp[i][j-1] + a), dp[i-1][j] + b);
				}
			}
		}
		return dp[n][m];
    }
};
//空间压缩
class Solution {
public:
    int minDistance(string word1, string word2) {
        int n = word1.size();
        int m = word2.size();
        int a = 1, b = 1, c = 1;
		// insert_cost = a, del_cost = b, replace_cost = c
		vector<int> dp1(m+1, 0);
        for (int i = 0; i<=m;i++){
            dp1[i] = i * a;
        }
		vector<int> dp2(m+1, 0);
		for (int i = 1; i<=n;i++){
            dp2[0] = i * b;//不要放到下面的循环内部，m == 0不进入那个分支
			for (int j = 1; j<=m;j++){
				if (word1[i-1] == word2[j-1]){
					dp2[j] = dp1[j-1];
				}
				else{
					dp2[j] = min(min(dp1[j-1] + c, dp2[j-1] + a), dp1[j] + b);
				}
			}
			for (int j = 0; j<=m; j++){
				dp1[j] = dp2[j];
			}
		}
		return dp1[m];
    }
};
```

## leetcode LCR 096. 交错字符串

[原题](https://leetcode.cn/problems/IY6buf/description/)

给定三个字符串 `s1`、`s2`、`s3`，请判断 `s3` 能不能由 `s1` 和 `s2` **交织（交错）** 组成。

两个字符串 `s` 和 `t` **交织** 的定义与过程如下，其中每个字符串都会被分割成若干 **非空** 子字符串：

- `s = s1 + s2 + ... + sn`
- `t = t1 + t2 + ... + tm`
- `|n - m| <= 1`
- **交织** 是 `s1 + t1 + s2 + t2 + s3 + t3 + ...` 或者 `t1 + s1 + t2 + s2 + t3 + s3 + ...`

**提示：**`a + b` 意味着字符串 `a` 和 `b` 连接。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2020/09/02/interleave.jpg)

```
输入：s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
输出：true
```

**示例 2：**

```
输入：s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
输出：false
```

**示例 3：**

```
输入：s1 = "", s2 = "", s3 = ""
输出：true
```



**提示：**

- `0 <= s1.length, s2.length <= 100`
- `0 <= s3.length <= 200`
- `s1`、`s2`、和 `s3` 都由小写英文字母组成

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int n = s1.size();
        int m = s2.size();
        if (s3.size() != n + m){
            return false;
        }
        vector<vector<int>> dp(n+1, vector<int>(m+1, 0));
        dp[0][0] = 1;
        for (int i = 1; i<=n;i++){
            if(s1[i-1] == s3[i-1]){
                dp[i][0] = 1;
			}
            else{
                break;
            }
		}
		for (int j = 1; j<=m;j++){
			if (s2[j-1] == s3[j-1]){
				dp[0][j] = 1;
			}
            else{
                break;
            }
		}
		for (int i = 1; i<=n;i++){
			for (int j = 1; j<=m;j++){
				if (s1[i-1] == s3[i+j-1]){
					dp[i][j] |= dp[i-1][j];//bool运算就用|
				}
				if (s2[j-1] == s3[i+j-1]){
					dp[i][j] |= dp[i][j-1];
				}
			}
		}
		return dp[n][m];
    }
};
//空间压缩
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int n = s1.size();
        int m = s2.size();
        if (s3.size() != n + m){
            return false;
        }
        vector<int> dp1(m+1, 0);
        vector<int> dp2(m+1, 0);
        dp1[0] = 1;
        for (int i = 1;i <= m;i++){
            if (s2[i-1] == s3[i-1]){
                dp1[i] = 1;
            }
            else{
                break;
            }
		}
		dp2[0] = 1;
		for (int i = 1; i<=n; i++){
            //一般放在j循环外面，防止出现空串进不了j循环
            dp2[0] = dp1[0] && s1[i-1] == s3[i-1];
			for(int j = 1; j<=m;j++){
                dp2[j] = 0; //必须显示清零，否则会有残余信息
				if (s1[i-1] == s3[i+j-1]) dp2[j] |= dp1[j];
				if (s2[j-1] == s3[i+j-1]) dp2[j] |= dp2[j-1];
			}
			for (int j = 0; j<=m;j++){
				dp1[j] = dp2[j];
			}
		}
		return dp1[m];
    }
};
```

## 有效涂色问题

给定n，m两个参数，一共有n个格子，每个格子可以涂上一种颜色，颜色在m种里选

当涂满n个格子的时候，并且m种颜色都使用了，叫一种有效方法

求一种有多少种有效的涂色方法

1 <= n, m <= 5000

结果比较大，请 % 1000000007 之后返回

```cpp
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define mod 1000000007
int n, m;
int main(){
	cin >> n >> m;
	//dp[i][j] : 当涂满i个格子，并且j种颜色都使用了，有多少种有效方法
	//dp[i][j] = dp[i-1][j] * j +  dp[i-1][j-1] * (m - j)
	//dp[0][j] : 当涂满0个格子，使用一定是0种颜色，所以dp[0][0] = 1; dp[0][j] = 0(j > 0)
	//dp[i][0] : 当涂满i个格子，使用0种颜色，不可能，dp[i][0] = 0(i > 0)
	vector<vector<ll>> dp(n+1, vector<ll> (m+1, 0));
	dp[0][0] = 1;
	for (int i = 1; i<=n;i++){
		for (int j = 1; j<=m;j++){
			dp[i][j] = ((dp[i-1][j] * j) % mod + (dp[i-1][j-1] * (m - j + 1)) % mod) % mod;
		}
	}
	cout << dp[n][m];
}
```

## 子串变换

删除**至少**几个字符可以变成另一个字符串的**子串**

给定两个字符串s1和s2

返回s1至少删除多少字符可以成为s2的子串

```cpp
#include<bits/stdc++.h>
using namespace std;
string s1, s2;
int main(){
	cin >> s1 >> s2;
	int n = s1.size();
	int m = s2.size();
	//dp[i][j] : s1[前i个前缀串] 想要变成s2[前j个字符组成的字符串的任意后缀串（以第j-1位置的字符结尾的后缀串）]至少需要删除几个字符
	//最后返回dp[n][j]一行中的最小值
	//dp[i][j] = 不相等dp[i-1][j] + 1 ,相等 dp[i-1][j-1]
	vector<vector<ll>> dp(n+1, vector<ll> (m+1, 0));
	for(int i = 1; i<=n;i++){
		dp[i][0] = i;
	}
	for (int i = 1; i<=n;i++){
		for (int j = 1; j<=m;j++){
			if (s1[i-1] == s2[j-1]){
				dp[i][j] = dp[i-1][j-1];
			}
			else{
				dp[i][j] = dp[i-1][j] + 1;
			}
		}
	}
	ll ans = 4890909195324358656;
	for (int i = 0; i<=m;i++){
		ans = min(ans, dp[n][i]);
	}
	cout << ans;
}
```

# 从递归入手三维动态规划

## leetcode 474. 一和零 - 力扣

[原题](https://leetcode.cn/problems/ones-and-zeroes/description/)

给你一个二进制字符串数组 `strs` 和两个整数 `m` 和 `n` 。

请你找出并返回 `strs` 的最大子集的长度，该子集中 **最多** 有 `m` 个 `0` 和 `n` 个 `1` 。

如果 `x` 的所有元素也是 `y` 的元素，集合 `x` 是集合 `y` 的 **子集** 。



**示例 1：**

```
输入：strs = ["10", "0001", "111001", "1", "0"], m = 5, n = 3
输出：4
解释：最多有 5 个 0 和 3 个 1 的最大子集是 {"10","0001","1","0"} ，因此答案是 4 。
其他满足题意但较小的子集包括 {"0001","1"} 和 {"10","1","0"} 。{"111001"} 不满足题意，因为它含 4 个 1 ，大于 n 的值 3 。
```

**示例 2：**

```
输入：strs = ["10", "0", "1"], m = 1, n = 1
输出：2
解释：最大的子集是 {"0", "1"} ，所以答案是 2 。
```



**提示：**

- `1 <= strs.length <= 600`
- `1 <= strs[i].length <= 100`
- `strs[i]` 仅由 `'0'` 和 `'1'` 组成
- `1 <= m, n <= 100`

 ```cpp
 //二维费用01背包
 int zeros, ones;
 class Solution {
 public:
    void zeros_and_ones(string str){
        // 统计一个字符串中0和1的数量
        zeros = 0;
        ones = 0;
        for (int i = 0; i<str.size();i++){
            if (str[i] == '0') zeros++;
            else ones++;
        }
    }
    // strs[i ……] 自由选择，希望0的数量不超过z,1的数量不超过o
    //最多能选多少个字符串
    int f1(vector<string> & strs, int i, int z, int o, vector<vector<vector<int>>>  & dp){
        if (i == strs.size()){
            //没有字符串了
            return 0;
        }
        if (dp[i][z][o] != -1){
            return dp[i][z][o];
        }
        // 不使用当前strs[i]字符串
        int p1 = f1(strs, i+1, z, o,dp);
        // 使用当前strs[i]字符串
        int p2 = 0;
        zeros_and_ones(strs[i]);
        if (zeros <= z && ones <= o){
            p2 = 1 + f1(strs, i+1, z - zeros, o - ones, dp);
        }
        dp[i][z][o] =  max(p1, p2);
        return dp[i][z][o];
    }
     int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<vector<int>>> dp(strs.size(), vector<vector<int>> (m+1, vector<int> (n+1, -1)));
         return f1(strs, 0, m, n, dp);
     }
 };
 //严格位置依赖
 int zeros, ones;
 class Solution {
 public:
    void zeros_and_ones(string str){
        // 统计一个字符串中0和1的数量
        zeros = 0;
        ones = 0;
        for (int i = 0; i<str.size();i++){
            if (str[i] == '0') zeros++;
            else ones++;
        }
    }
     int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<vector<int>>> dp(strs.size() + 1, vector<vector<int>> (m+1, vector<int> (n+1, 0)));
         for (int i = strs.size() - 1; i>=0 ;i--){

            for (int z = 0, p1, p2; z<=m;z++){
                for (int o = 0; o<=n;o++){
                    p1 = dp[i+1][z][o];//不选
                    p2 = 0;
                     zeros_and_ones(strs[i]);
                    if (zeros <= z && ones <= o){
                        p2 = dp[i+1][z - zeros][o - ones] + 1;//选
                    }
                    dp[i][z][o] = max(p1, p2);
                }
            }
        }
        return dp[0][m][n];
     }
 };
 //空间压缩
 //必须倒着来，因为所有的都依赖上一层的数据，而如果从小到大遍历会改变上一层的数据
 int zeros, ones;
 class Solution {
 public:
    void zeros_and_ones(string  & str){
        // 统计一个字符串中0和1的数量
        zeros = 0;
        ones = 0;
        for (int i = 0; i<str.size();i++){
            if (str[i] == '0') zeros++;
            else ones++;
        }
    }
     int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<int>> dp(m+1, vector<int> (n+1, 0));
        for (int i = strs.size() - 1;i>=0;i--){
            for (int o = n, p1, p2; o>=0;o--){
                for (int z = m; z>=0;z--){
                    p1 = dp[z][o];
                    p2 = 0;
                    zeros_and_ones(strs[i]);
                    if (zeros <= z && ones <= o){
                        p2 = dp[z - zeros][o - ones] + 1;
                    }
                    dp[z][o] = max(p1, p2);
                }
            }
        }
        return dp[m][n];
     }
 };
 //左神版本
 int zeros, ones;
 class Solution {
 public:
    void zeros_and_ones(string  & str){
        // 统计一个字符串中0和1的数量
        zeros = 0;
        ones = 0;
        for (int i = 0; i<str.size();i++){
            if (str[i] == '0') zeros++;
            else ones++;
        }
    }
     int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<int>> dp(m+1, vector<int> (n+1, 0));
        for (string s : strs){
             zeros_and_ones(s);
            for (int o = n; o>=ones;o--){//如果o<ones，那么不改变dp[z][o]就行，即不需要任何操作
                for (int z = m; z >= zeros;z--){
                    dp[z][o] = max(dp[z][o], dp[z-zeros][o-ones] + 1);
                }
            }
        }
        return dp[m][n];
     }
 };
 ```

## leetcode 879. 盈利计划 - 力扣

[原题](https://leetcode.cn/problems/profitable-schemes/description/)

集团里有 `n` 名员工，他们可以完成各种各样的工作创造利润。

第 `i` 种工作会产生 `profit[i]` 的利润，它要求 `group[i]` 名成员共同参与。如果成员参与了其中一项工作，就不能参与另一项工作。

工作的任何至少产生 `minProfit` 利润的子集称为 **盈利计划** 。并且工作的成员总数最多为 `n` 。

有多少种计划可以选择？因为答案很大，所以 **返回结果模** `10^9 + 7` **的值**。



**示例 1：**

```
输入：n = 5, minProfit = 3, group = [2,2], profit = [2,3]
输出：2
解释：至少产生 3 的利润，该集团可以完成工作 0 和工作 1 ，或仅完成工作 1 。
总的来说，有两种计划。
```

**示例 2：**

```
输入：n = 10, minProfit = 5, group = [2,3,5], profit = [6,7,8]
输出：7
解释：至少产生 5 的利润，只要完成其中一种工作就行，所以该集团可以完成任何工作。
有 7 种可能的计划：(0)，(1)，(2)，(0,1)，(0,2)，(1,2)，以及 (0,1,2) 。
```



**提示：**

- `1 <= n <= 100`
- `0 <= minProfit <= 100`
- `1 <= group.length <= 100`
- `1 <= group[i] <= 100`
- `profit.length == group.length`
- `0 <= profit[i] <= 100`

```cpp
#define mod 1000000007
using ll = long long;
class Solution {
public:
	// i : 来到i号工作
	// r : 员工额度还有r人，如果r<=0说明已经没法再选工作了
	// s : 利润还有s才能达标，如果s<=0说明之前的选择已经让利润达标了
	int f1(vector<int> & g, vector<int> & p, int i, int r, int s,vector<vector<vector<int>>> & dp){
		if (r <= 0){
			//人已经耗尽了，之前可能选了一些工作
			return s<=0 ? 1 : 0;
		}
		// r > 0
		if (i == g.size()){
			//工作耗尽了，之前可能选了一些工作
			return s <= 0 ? 1 : 0;
		}
		if (dp[i][r][s] != -1) return dp[i][r][s];
		int p1, p2 = 0;
		//之前做了一些选择，不要当前工作
		p1 = f1(g, p, i+1, r, s, dp);
		//要做当前工作
		if (g[i] <= r){
            //利润可能为负数
            int ns = max(0, s - p[i]);
			p2 = f1(g, p, i+1, r - g[i], ns, dp);
		}
		int ans = (p1 % mod + p2 % mod) % mod;
		dp[i][r][s] = ans;
		return ans;
	}
    int profitableSchemes(int n, int minProfit, vector<int>& group, vector<int>& profit) {
        vector<vector<vector<int>>> dp(group.size(), vector<vector<int>> (n + 1, vector<int> (minProfit + 1, -1)));
        return f1(group, profit, 0, n, minProfit, dp);
    }
};
```
