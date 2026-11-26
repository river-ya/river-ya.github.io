# 1.递归
## 1.1 递归初步介绍
在递归过程中，当发现无法执行下去的时候，其中的**参数位，函数状态，中间结果**都会保留在系统栈里
但是平时写递归可以画递归调用图，而不是系统栈（系统栈空间）（贵的）
所有的递归都可以用非递归写法模拟，即自己在自己的内存空间（便宜的）里建一个栈模拟，可能消耗的空间没有系统栈那么大，也能避免系统栈太深导致出错
递归改成非递归的必要性：

* 工程上几乎一定要改，除非确定数据量再大递归也一定不深，归并排序（O(log n)）、快速排序、线段树、很多的平衡树等
* 算法笔试或者比赛中能通过就不改
## 1.2 master公式
1. 所有子问题规模相同的递归才能用master公式，a，b，c都是常数
$ T(N) = a * T(\frac{N}{b}) + O(N^c) $
2. 当 $ \log_b a > c$ 时，时间复杂度为 $ O(N^{\log_b a})$
3. 当 $ \log_b a < c$ 时，时间复杂度为 $ O(N^c)$(直观理解就是谁大选谁)
4. 当 $ \log_b a = c$ 时，时间复杂度为 $ O(N^c * \log N)$
5. 补充（不是master公式）：$ T(N) = 2 * T(\frac{N}{2}) + O(N * \log N)$,时间复杂度是 $ O(N * (\log N)^2)$,证明略
## 1.3 常见经典递归过程

T1 - T4是带路径的递归，T5-T6是不带路径的递归

### T1 [字符串的全部子序列 newcode NC190](https://www.nowcoder.com/practice/92e6247998294f2c933906fdedbc6e6a?tpId=196&tqId=39357&ru=/exam/oj)
给定一个字符串s，长度为n，求s的所有子序列
1.子序列: 指一个字符串删掉部分字符（也可以不删）形成的字符串，可以是不连续的，比如"abcde"的子序列可以有"ace","ad"等等
2.将所有的子序列的结果返回为一个字符串数组
3.字符串里面可能有重复字符，但是返回的子序列不能有重复的子序列，比如"aab"的子序列只有"","a","aa","aab","ab","b"，不能存在2个相同的"ab"
4.返回字符串数组里面的顺序可以不唯一

数据范围:
0<=s.length<=16
0<=s.length<=16

要求:时间复杂度为
O（2^n）

```cpp
//时间复杂度： O(n * 2 ^ n)
//写法一：显示恢复原样，也就是回溯
class Solution {
public:
    set<string> st;
    string path;
    void f(string s, int i){
        if (i == s.size()){
            st.insert(path);
        }
        else{
            //选了字符
            path.push_back(s[i]);
            f(s, i+1);
            //恢复原样，没选字符
            path.erase(path.size() - 1);
            f(s, i+1);
        }
    }
    vector<string> generatePermutation(string s) {
        f(s, 0);
        vector<string> ans(st.begin(), st.end());
        return ans;
    }
};
//写法二：类似栈的手搓，我只需要size来控制长度，其余垃圾值不会读取
class Solution {
public:
    set<string> st;
    string path;
    void f(string s, int i,int size){
        if (i == s.size()){
            st.insert(path.substr(0, size));//选取前size个字符
        }
        else{
            path[size] = s[i];
            f(s, i+1, size + 1);//选了字符
            f(s, i+1, size);//没选字符
        }
    }
    vector<string> generatePermutation(string s) {
        path.resize(s.size());//记得resize path
        f(s, 0, 0);
        vector<string> ans(st.begin(), st.end());
        return ans;
    }
};
```

**总结：由于在本题中path是全局变量，故需要回溯恢复原状态**

**如果将path变成值传递，那么将不需要手动回溯，但是这样往往时间空间开销会很大，每次都需要拷贝O(n)时间的path，同时还会增加额外空间，所以一般我们采取回溯+址传递/全局变量**

###  [T2 子集II leetcode No.90](https://leetcode.cn/problems/subsets-ii/description/)

给你一个整数数组 `nums` ，其中可能包含重复元素，请你返回该数组所有可能的 子集（幂集）。

解集 **不能** 包含重复的子集。返回的解集中，子集可以按 **任意顺序** 排列。

**示例 1：**

```
输入：nums = [1,2,2]
输出：[[],[1],[1,2],[1,2,2],[2],[2,2]]
```

**示例 2：**

```
输入：nums = [0]
输出：[[],[0]]
```

**提示：**

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`

本题我将详细讲述什么时候需要回溯，什么时候不需要回溯

先看不需要回溯的版本

```cpp
//注意这是个组合，而不是排列
    vector<vector<int>> ans;
    void f(int i, vector<int> & nums, vector<int> path){//注意这里的path是值引用，每次都copy
        if(i == nums.size()){
            ans.push_back(path);
            return;
        }
        int j = i + 1;
        //找下一个数字的第一个位置
        while(j < nums.size() && nums[i] == nums[j]){
            j++;
        }
        //0个数字
        f(j, nums,path);
        //1-cnt个数字
        for (;i<j;i++){
            path.push_back(nums[i]);
            f(j, nums, path);
        }
        //没有回溯
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        //可排可不排，排序之后可以剪枝，而不是利用set过滤去重
        sort(nums.begin(), nums.end());
        ans.clear();
        vector<int> path;
        f(0, nums,path);
        return ans;
    }
```

再看回溯版本

```cpp
vector<vector<int>> ans;
    void f(int i, vector<int> & nums, vector<int> & path){//注意这里path是址引用，需要回溯
        if(i == nums.size()){
            ans.push_back(path);
            return;
        }
        int j = i + 1;
        while(j < nums.size() && nums[i] == nums[j]){
            j++;
        }
        int cnt = j - i;//记录次数
        f(j, nums,path);
        for (;i<j;i++){
            path.push_back(nums[i]);
            f(j, nums, path);
        }
        for(int k = 0;k<cnt;k++){//回溯
            path.pop_back();
        }
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        //可排可不排，排序之后可以剪枝，而不是利用set过滤去重
        sort(nums.begin(), nums.end());
        ans.clear();
        vector<int> path;
        f(0, nums,path);
        return ans;
    }
```

### [T3 全排列 leetcode LCR 083](https://leetcode.cn/problems/VvJkup/description/)

给定一个不含重复数字的整数数组 `nums` ，返回其 **所有可能的全排列** 。可以 **按任意顺序** 返回答案。

**示例 1：**

```
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**示例 2：**

```
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

**示例 3：**

```
输入：nums = [1]
输出：[[1]]
```

**提示：**

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- `nums` 中的所有整数 **互不相同**

```cpp
vector<vector<int>> ans;
    void f(vector<int> & nums, int i){
        if (i == nums.size()){
            ans.push_back(nums);
            return;
        }
        for (int j = i;j<nums.size();j++){
            swap(nums[i], nums[j]);
            f(nums,i+1);
            swap(nums[i],nums[j]);//回溯换回原状态
        }
    }
    vector<vector<int>> permute(vector<int>& nums) {
        ans.clear();
        f(nums, 0);
        return ans;
    }
```
### [T4 全排列II leetcode LCR 084](https://leetcode.cn/problems/7p8L0Z/description/)

给定一个可包含重复数字的整数集合 `nums` ，**按任意顺序** 返回它所有不重复的全排列。

**示例 1：**

```
输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]
```

**示例 2：**

```
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**提示：**

- `1 <= nums.length <= 8`
- `-10 <= nums[i] <= 10`

```cpp
    vector<vector<int>> ans;
    void f(vector<int> & nums, int i){
        if (i == nums.size()){
            ans.push_back(nums);
            return;
        }
        unordered_set<int> st;//去重集合
        for (int j = i;j<nums.size();j++){
            if (!st.count(nums[j])){//如果该数字已经来过这个位置则跳过
                st.insert(nums[j]);
                swap(nums[i], nums[j]);
                f(nums,i+1);
                swap(nums[i],nums[j]);//回溯换回原状态
            }
        }
    }
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        ans.clear();
        f(nums, 0);
        return ans;
    }
```



### T5 用递归逆序一个栈

```cpp
//栈底弹出，其余元素盖下来
int bottomout(stack<int> & stk){
    int ans = stk.top();
    stk.pop();
    if (stk.empty()){
        return ans;
    }
    int last = bottomout(stk);
    stk.push(ans);
    return last;
}
void reverse_stack(stack<int> & stk){
    if (stk.empty()){
        return;
    }
    int num = bottomout(stk);
    reverse_stack(stk);
    stk.push(num);
}
```

### T6 用递归排序一个栈

```cpp
int deep(stack<int> & stk){
    if (stk.empty()){
        return 0;
    }
    int num = stk.top();
    stk.pop();
    int d = deep(stk) + 1;
    stk.push(num);
    return d;
}
int Max(stack<int> & stk){
    if (stk.empty()){
        return INT_MIN;
    }
    int num = stk.top();
    stk.pop();
    int rest_max = Max(stk);
    int cur_max = max(rest_max, num);
    stk.push(num);
    return cur_max;
}
int Time(stack<int> & stk, int max_val){
    if (stk.empty()){
        return 0;
    }
    int num = stk.top();
    stk.pop();
    int rest_time = Time(stk, max_val);
    int cur_time = (num == max_val ? 1 : 0) + rest_time;
    stk.push(num);
    return cur_time;
}
void down(stack<int> & stk, int max_val, int times){
    if (stk.empty()){
        for (int i = 0;i<times;i++){
            stk.push(max_val);
        }
        return;
    }
    int num = stk.top();
    stk.pop();
    down(stk, max_val, times);
    if (num != max_val){
        stk.push(num);
    }
}
//用递归排序一个栈
void Sort_recursion(stack<int> & stk){
    //求栈深
    int depth = deep(stk);
    while(depth > 0){
        int max_val = Max(stk);
        int times = Time(stk, max_val);
        down(stk, max_val, times);
        depth -= times;
    }
}
```

## 1.4 嵌套类递归问题

### 嵌套类递归问题的解决套路

大概过程：

1. 定义**全局变量 where**
2. 递归函数f(i)：s[i……] 从i位置开始解析，遇到**字符串终止**或**嵌套条件终止**就返回
3. 返回值是f(i)负责这一段的结果
4. f(i)在**返回前更新**全局变量where，让上级函数通过where知道解析到了什么位置，进而继续

执行细节：

1. 如果f(i)遇到嵌套条件开始，就调用下级递归去处理嵌套，下级会负责嵌套部分的计算结果
2. f(i)下级处理完成后，f(i)可以根据下级更新的全局变量where，知道从什么位置继续解析

### [T1 leetcode 基本计算器III](https://leetcode.cn/problems/basic-calculator-iii)

实现一个基本的计算器来计算简单的表达式字符串。

表达式字符串只包含非负整数，算符 +、-、*、/ ，左括号 ( 和右括号 ) 。整数除法需要 向下截断 。

你可以假定给定的表达式总是有效的。所有的中间结果的范围为 [-2^31, 2^31 - 1] 。

**示例 1：**

输入：s = "1+1"
输出：2
**示例 2：**

输入：s = "6-4/2"
输出：4
**示例 3：**

输入：s = "2*(5+5*2)/3+(6/2+8)"
输出：21
**示例 4：**

输入：s = "(2+6*3+5-(3*14/7+2)*5)+3"
输出：-12
**示例 5：**

输入：s = "0"
输出：0


**提示：**

1 <= s <= 10^4
s 由整数、'+'、'-'、'*'、'/'、'(' 和 ')' 组成
s 是一个 有效的 表达式

```cpp
//由于我没有充plus会员，所以是自己手动评测
//时间复杂度 ： O(n)
#include <bits/stdc++.h>
using namespace std;
string s;
int where;
void poll(vector<int> & num, vector<char> & ops, char c, int a){
    if (ops.empty() && num.empty()){
        ops.push_back(c);
        num.push_back(a);
        return;
    }
    int op = ops.back();
    if (op == '*' || op == '/'){
        ops.pop_back();
        int n = num.back();
        num.pop_back();
        if (op == '*'){
            num.push_back(n * a);
            ops.push_back(c);
        }
        else if (op == '/'){
            num.push_back(n / a);
            ops.push_back(c);
        }
    }
    else{
        ops.push_back(c);
        num.push_back(a);
    }
    return;
}
int compute(vector<int> & num, vector<char> & ops){
    int n = num.size();
    int ans = num[0];
    for (int i = 0;i<n-1;i++){
        ans += (ops[i] == '+' ? 1 : -1) * num[i+1];
    }
    return ans;
}
//s[i…………]开始计算，遇到字符串末尾或)停止
//返回：自己负责的这一段计算的结果
//返回之前，更新全局变量where，为了让上游函数知道从哪继续
int f(int i){
    vector<int> num;//数字栈
    vector<char> ops;//符号栈
    int a = 0;
    while(i < s.size() && s[i] != ')'){//顺序不可变，不然会越界
        if (isdigit(s[i])){
            a = a * 10 + s[i] - '0';
        }
        else if (s[i] != '('){
            //遇到了运算符号
            poll(num, ops, s[i], a);
            a = 0;
        }
        else{
            //遇到了左括号
            a = f(i+1);
            i = where;
        }
        i++;
    }
    //最后一个数字由于没有后面的符号就结束了，所以还没有push进去，需要额外处理一下
    poll(num, ops, '+', a);
    where = i;
    return compute(num, ops);
}
int main(){
    cin >> s;
    int x = f(0);
    cout << x << endl;
    return 0;
}
```

### [T2 leetcode No.394 字符串解码](https://leetcode.cn/problems/decode-string/description/)

给定一个经过编码的字符串，返回它解码后的字符串。

编码规则为: `k[encoded_string]`，表示其中方括号内部的 `encoded_string` 正好重复 `k` 次。注意 `k` 保证为正整数。

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 `k` ，例如不会出现像 `3a` 或 `2[4]` 的输入。

测试用例保证输出的长度不会超过 `105`。



**示例 1：**

```
输入：s = "3[a]2[bc]"
输出："aaabcbc"
```

**示例 2：**

```
输入：s = "3[a2[c]]"
输出："accaccacc"
```

**示例 3：**

```
输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"
```

**示例 4：**

```
输入：s = "abc3[cd]xyz"
输出："abccdcdcdxyz"
```



**提示：**

- `1 <= s.length <= 30`
- `s` 由小写英文字母、数字和方括号 `'[]'` 组成
- `s` 保证是一个 **有效** 的输入。
- `s` 中所有整数的取值范围为 `[1, 300]`

```cpp
#include <bits/stdc++.h>
using namespace std;
string s;
int where;
string f(int i){
    int a = 0;
    string letters = "";
    while(i < s.size() && s[i] != ']'){
        if (isdigit(s[i])){
            a = a * 10 + s[i] - '0';
        }
        else if (s[i] != '['){
            letters += s[i];
        }
        else{
            string sub = f(i+1);
            while(a--){
                letters += sub;
            }
            a = 0;
            i = where;
        }
        i++;
    }
    where = i;
    return letters;
}
int main(){
    cin >> s;
    cout << f(0) << endl;
    return 0;
}
```

### [T3 leetcode No.726 原子的数量](https://leetcode.cn/problems/number-of-atoms/description/)

给你一个字符串化学式 `formula` ，返回 **每种原子的数量** 。

原子总是以一个大写字母开始，接着跟随 0 个或任意个小写字母，表示原子的名字。

如果数量大于 1，原子后会跟着数字表示原子的数量。如果数量等于 1 则不会跟数字。

- 例如，`"H2O"` 和 `"H2O2"` 是可行的，但 `"H1O2"` 这个表达是不可行的。

两个化学式连在一起可以构成新的化学式。

- 例如 `"H2O2He3Mg4"` 也是化学式。

由括号括起的化学式并佐以数字（可选择性添加）也是化学式。

- 例如 `"(H2O2)"` 和 `"(H2O2)3"` 是化学式。

返回所有原子的数量，格式为：第一个（按字典序）原子的名字，跟着它的数量（如果数量大于 1），然后是第二个原子的名字（按字典序），跟着它的数量（如果数量大于 1），以此类推。



**示例 1：**

```
输入：formula = "H2O"
输出："H2O"
解释：原子的数量是 {'H': 2, 'O': 1}。
```

**示例 2：**

```
输入：formula = "Mg(OH)2"
输出："H2MgO2"
解释：原子的数量是 {'H': 2, 'Mg': 1, 'O': 2}。
```

**示例 3：**

```
输入：formula = "K4(ON(SO3)2)2"
输出："K4N2O14S4"
解释：原子的数量是 {'K': 4, 'N': 2, 'O': 14, 'S': 4}。
```



**提示：**

- `1 <= formula.length <= 1000`
- `formula` 由英文字母、数字、`'('` 和 `')'` 组成
- `formula` 总是有效的化学式

```cpp
//leetcode一直登不上去，不理解（，只能这样写了
#include <bits/stdc++.h>
using namespace std;
string s;
map<string,int> ans;
int where;
void finish(map<string, int> & tot, map<string, int> & history1, string & history2, int & cnt){
    if (!history1.empty() || history2 != "")
    {
    cnt = ((cnt == 0) ? 1 : cnt);
    if (history2 != ""){
        tot[history2] += cnt;
        cnt = 0;
        history2 = "";
    }
    else if(!history1.empty()){
        for (const auto & pr : history1){
            tot[pr.first] += (cnt * pr.second);
        }
        cnt = 0;
        history1.clear();
    }
    }
    return;
}
map<string, int> f(int i){
    map<string, int> tot;
    //旧的表
    map<string,int> history1;
    //旧的元素
    string history2;
    int cnt = 0;
    while(i < s.size() && s[i] != ')'){
        //遇到大写字母和左括号意味着：旧的历史要结算，新的东西要记录
        if (s[i] >= 'A' && s[i] <= 'Z' || s[i] == '('){
            finish(tot, history1, history2, cnt);
            if (s[i] >= 'A' && s[i] <= 'Z'){
                history2 = s[i];
            }
            else{
                history1 = f(i+1);
                i = where;
            }
        }
        else if (s[i] >= 'a' && s[i] <= 'z'){
            history2 += s[i];
        }
        else{
            cnt = cnt * 10 + s[i] - '0';
        }
        i++;
    }
    finish(tot, history1, history2, cnt);
    where = i;
    return tot;
}
int main(){
    cin >> s;
    ans = f(0);
    for (const auto & pr : ans){
        cout << pr.first << ((pr.second==1)?"":to_string(pr.second));
    }
    return 0;
}
```

## 1.5 N皇后问题

数组dfs模拟,可以过,但常数时间慢

```cpp
#include <bits/stdc++.h>
using namespace std;
int n;
bool check(vector<int> & path, int i, int j){
    if (i == 0) return true;
    for (int k = 0;k<i;k++){
        if (path[k] == j || abs(path[k] - j) == abs(k - i)){
            return false;
        }
    }
    return true;
}
//i表示当前来到的行，path数组放[0, i-1]行的皇后放在第path[i]列
int f(int i, vector<int> & path){
    if(i == n){
        return 1;
    }
    int ans = 0;
    for (int j = 0;j<n;j++){
        if (check(path, i, j)){
            path[i] = j;
            ans += f(i+1, path);//为什么不回溯？因为我的check函数只考虑前i个数字，而且每次回到循环的时候都会覆盖掉path的最新值
        }
    }
    return ans;
}
int main(){
    cin >> n;
    vector<int> path (n, 0);
    cout << f(0, path);
}
```

位运算版本,常数级很快

```cpp
#include <bits/stdc++.h>
using namespace std;
int n;
unsigned limit;
//limit：当前是几皇后问题
//之前皇后的列影响：col
//之前皇后的右上->左下对角线影响： left
//之前皇后的左上->右下对角线影响：right
//初探状态迁移
int f(unsigned col, unsigned left, unsigned right){//不带行的限制
    if (col == limit){
        //所有皇后放完了
        return 1;
    }
    //总限制
    int ban = col | left | right;
    int ans = 0;
    //~ban： 1可放皇后，0不能放(因为需要限制范围，而范围之外默认为0)
    int pos = limit & (~ban);//放置皇后的尝试
    while(pos){
        int place = pos & (-pos);//依次提取最右侧的1
        pos ^= place;//和减法一样的效果
        ans += f(col | place, (left|place) >> 1, (right|place) << 1);
    }
    return ans;
}
int main(){
    cin >> n;
    //n = 5
    //limit = 0……011111
    limit = (1 << n) - 1;//规定范围，状态限制
    cout << f(0u, 0u, 0u);
}
```



## P1928 外星密码

[洛谷 P1928](https://www.luogu.com.cn/problem/P1928)


### 题目描述

有了防护伞，并不能完全避免 2012 的灾难。地球防卫小队决定去求助外星种族的帮助。经过很长时间的努力，小队终于收到了外星生命的回信。但是外星人发过来的却是一串密码。只有解开密码，才能知道外星人给的准确回复。解开密码的第一道工序就是解压缩密码，外星人对于连续的若干个相同的子串 $\texttt{X}$ 会压缩为 $\texttt{[DX]}$ 的形式（$D$ 是一个整数且 $1\leq D\leq99$），比如说字符串 $\texttt{CBCBCBCB}$ 就压缩为 $\texttt{[4CB]}$ 或者$\texttt{[2[2CB]]}$，类似于后面这种压缩之后再压缩的称为二重压缩。如果是 $\texttt{[2[2[2CB]]]}$ 则是三重的。现在我们给你外星人发送的密码，请你对其进行解压缩。

### 输入格式

输入一行，一个字符串，表示外星人发送的密码。

### 输出格式

输出一行，一个字符串，表示解压缩后的结果。

### 输入输出样例 #1

#### 输入 #1

```
AC[3FUN]
```

#### 输出 #1

```
ACFUNFUNFUN
```

### 说明/提示

【数据范围】

对于 $50\%$ 的数据：解压后的字符串长度在 $1000$ 以内，最多只有三重压缩。

对于 $100\%$ 的数据：解压后的字符串长度在 $20000$ 以内，最多只有十重压缩。保证只包含数字、大写字母、`[` 和 `]`。
```cpp
#include <bits/stdc++.h>
using namespace std;
string expand()
{
    string ans = "", recursion;
    char c;
    int D;
    while (cin >> c)
    {
        if (c == '[')
        {
            cin >> D;
            recursion = expand();
            while (D--) ans += recursion;
        }
        else if (c == ']') return ans;
        else ans += c;
    }
    return ans;
}
int main()
{
    cout << expand();
    return 0;
}
```

## P5461 赦免战俘

[洛谷 P5461](https://www.luogu.com.cn/problem/P5461)


### 题目背景

借助反作弊系统，一些在月赛有抄袭作弊行为的选手被抓出来了！

### 题目描述

现有 $2^n\times 2^n (n\le10)$ 名作弊者站成一个正方形方阵等候 kkksc03 的发落。kkksc03 决定赦免一些作弊者。他将正方形矩阵均分为 $4$ 个更小的正方形矩阵，每个更小的矩阵的边长是原矩阵的一半。其中左上角那一个矩阵的所有作弊者都将得到赦免，剩下 $3$ 个小矩阵中，每一个矩阵继续分为 $4$ 个更小的矩阵，然后通过同样的方式赦免作弊者……直到矩阵无法再分下去为止。所有没有被赦免的作弊者都将被处以棕名处罚。

给出 $n$，请输出每名作弊者的命运，其中 $0$ 代表被赦免，$1$ 代表不被赦免。

### 输入格式

一个整数 $n$。

### 输出格式

$2^n \times 2^n$ 的 01 矩阵，代表每个人是否被赦免。数字之间有一个空格。

### 输入输出样例 #1

#### 输入 #1

```
3
```

#### 输出 #1

```
0 0 0 0 0 0 0 1
0 0 0 0 0 0 1 1
0 0 0 0 0 1 0 1
0 0 0 0 1 1 1 1
0 0 0 1 0 0 0 1
0 0 1 1 0 0 1 1
0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1
```
```cpp
#include <bits/stdc++.h>
using namespace std;
int arr[1100][1100], n;
void cal(int x, int y, int n)
{
    if (!n) arr[x][y] = 1;
    else
    {
        cal(x + (1 << n-1), y, n - 1);
        cal(x, y + (1 << n - 1), n - 1);
        cal(x + (1 << n - 1), y + (1 << n -1), n - 1);
    }
}
int main(){
    scanf("%d", &n);
    cal(0, 0, n);
    for (int i = 0; i < pow(2, n); i++)
    {
        for (int j = 0; j < pow(2, n); j++)
        {
            printf("%d ", arr[i][j]);
        }
        cout << endl;
    }
    return 0;
}
```
