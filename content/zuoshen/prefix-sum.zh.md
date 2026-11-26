# 前缀和

## 构建前缀信息的技巧(解决子数组相关问题)

前缀和数组构建

```cpp
vector<int> sum(n+1, 0);
for (int i = 1;i<=nums.size();i++){
    sum[i] = sum[i-1] + nums[i-1];
}
int sumrange(int left, int right){//left和right是索引,[left, right]的区间和
    return sum[right + 1] - sum[left];
}
```

### [T1 和等于k的最长子数组长度 newcode](https://www.nowcoder.com/practice/704c8388a82e42e58b7f5751ec943a11)

给定一个无序数组 arr , 其中元素可正、可负、可0。给定一个整数 k ，求 arr 所有连续子数组中累加和为k的最长连续子数组长度。保证至少存在一个合法的连续子数组。

[1,2,3]的连续子数组有[1,2]，[2,3]，[1,2,3] ，但是[1,3]不是

数据范围： 1≤n≤105，∣*v**a**l*∣≤100，∣*k*∣≤109
要求：空间复杂度 O(n)， 时间复杂度 O(n)

示例1

输入：

```
[1,-2,1,1,1],0
```


返回值：

```
3
```

示例2

输入：

```
[0,1,2,3],3
```

返回值：

```
3
```


备注：

```
1⩽N⩽105
−109⩽k⩽109
−100⩽arri⩽100
```

首先是我第一次的想法,时间复杂度O(n^2^)

```cpp
#include <bits/stdc++.h>
using namespace std;
int n, target;
vector<int> nums;
int main(){
    cin >> n >> target;
    nums.resize(n);
    for (int i = 0;i<n;i++){
        cin >> nums[i];
    }
    vector<int> sum(n+1, 0);
    for (int i = 1;i<=n;i++){
        sum[i] = sum[i-1] + nums[i-1];
    }
    int maxlen = 0;
    for (int i = n;i>=0;i--){
        for (int j = 0;j<=i;j++){
            if (sum[i] - sum[j] == target){
                maxlen = max(maxlen, i - j);
                break;
            }
        }
    }
    cout << maxlen << endl;
    return 0;
}
```

接下来是左神的想法,时间复杂度:O(n)

```cpp
#include <bits/stdc++.h>
using namespace std;
int n, target;
vector<int> nums;
int main(){
    cin >> n >> target;
    nums.resize(n);
    for (int i = 0;i<n;i++){
        cin >> nums[i];
    }
    int maxlen = 0;
    //key : 0 …… key 的前缀和
    //value : 最早出现key的索引位置
    unordered_map<int, int> ump;
    ump[0] = -1;
    //重要：避免漏掉左侧边界在0位置的情况,0这个位置的累加和，一个数字都没有的时候就存在了
    for (int i = 0, sum = 0;i<n;i++){//sum表示整体累加和
        sum += nums[i];
        //sum - target 最早出现的位置
        if (ump.count(sum - target)){
            maxlen = max(maxlen, i - ump[sum - target]);
        }
        //只记录最早出现的位置，出现过了就不更新了
        if (!ump.count(sum)){
            ump[sum] = i;
        }
    }
    cout << maxlen << endl;
    return 0;
}
//再挂一个测试版
class Solution {
public:
    int maxlenEqualK(vector<int>& arr, int k) {
        unordered_map<int, int> ump;
        ump[0] = -1;
        int ans = 0;
        for (int i = 0, sum = 0; i<arr.size(); i++){
            sum += arr[i];
            if (ump.count(sum - k)){
                ans = max(ans, i - ump[sum - k]);
            }
            if (!ump.count(sum)){
                ump[sum] = i;
            }
        }
        return ans;
    }
};
```

变形:构建前缀和最早出现的位置,返回无序数组中正数和负数个数相等的最长子数组长度

只需要利用符号函数将正负数区分开,剩下的和本题一模一样

### [T2 和为K的子数组 leetcode LCR 010](https://leetcode.cn/problems/QTMn0o/description/)

给定一个整数数组和一个整数 `k` **，**请找到该数组中和为 `k` 的连续子数组的个数。



**示例 1：**

```
输入:nums = [1,1,1], k = 2
输出: 2
解释: 此题 [1,1] 与 [1,1] 为两种不同的情况
```

**示例 2：**

```
输入:nums = [1,2,3], k = 3
输出: 2
```



**提示:**

- `1 <= nums.length <= 2 * 104`
- `-1000 <= nums[i] <= 1000`
- `-107 <= k <= 107`

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        int ans = 0;
        unordered_map<int, int> ump;
        ump[0] = 1;
        for (int i = 0, sum = 0; i<nums.size();i++){
            sum += nums[i];
            if (ump.count(sum - k)){
                ans += ump[sum - k];
            }
            ump[sum]++;
        }
        return ans;
    }
};
```

### [T3 表现良好的最长时间段 leetcode No.1124](https://leetcode.cn/problems/longest-well-performing-interval/description/)

给你一份工作时间表 `hours`，上面记录着某一位员工每天的工作小时数。

我们认为当员工一天中的工作小时数大于 `8` 小时的时候，那么这一天就是「**劳累的一天**」。

所谓「表现良好的时间段」，意味在这段时间内，「劳累的天数」是严格 **大于**「不劳累的天数」。

请你返回「表现良好时间段」的最大长度。



**示例 1：**

```
输入：hours = [9,9,6,0,6,6,9]
输出：3
解释：最长的表现良好时间段是 [9,9,6]。
```

**示例 2：**

```
输入：hours = [6,6,6]
输出：0
```



**提示：**

- `1 <= hours.length <= 104`
- `0 <= hours[i] <= 16`

```cpp
class Solution {
public:
    int longestWPI(vector<int>& hours) {
        unordered_map<int, int> ump;
        ump[0] = -1;
        int ans = 0;
        for (int i = 0, sum = 0;i<hours.size();i++){
            sum += (hours[i] > 8) ? 1 : -1;
            if (sum > 0){
                ans = i + 1;
            }//这个if判断不能省略,如果这个hours中的元素都大于8,那么如果去掉这个if的话,就会返回1这个错误答案
            else{
                // 比如 sum = -3, 那么我只需要找-4最早出现的位置即可,为什么不找-5,-6~~~?
                //因为如果前面有-5出现,代表前面一定也有-4出现,(0 -> -5) 一定会经过-4
                if (ump.count(sum - 1)){//sum一定是连续的函数,不会有突变,这是变成1,-1之后很重要的性质
                    ans = max(ans,  i - ump[sum - 1]);
                }
                if (!ump.count(sum)){
                    ump[sum] = i;
                }
            }
        }
        return ans;
    }
};
```

### [T4 使数组和能被P整除 leetcode No.1590](https://leetcode.cn/problems/make-sum-divisible-by-p/)

给你一个正整数数组 `nums`，请你移除 **最短** 子数组（可以为 **空**），使得剩余元素的 **和** 能被 `p` 整除。 **不允许** 将整个数组都移除。

请你返回你需要移除的最短子数组的长度，如果无法满足题目要求，返回 `-1` 。

**子数组** 定义为原数组中连续的一组元素。



**示例 1：**

```
输入：nums = [3,1,4,2], p = 6
输出：1
解释：nums 中元素和为 10，不能被 p 整除。我们可以移除子数组 [4] ，剩余元素的和为 6 。
```

**示例 2：**

```
输入：nums = [6,3,5,2], p = 9
输出：2
解释：我们无法移除任何一个元素使得和被 9 整除，最优方案是移除子数组 [5,2] ，剩余元素为 [6,3]，和为 9 。
```

**示例 3：**

```
输入：nums = [1,2,3], p = 3
输出：0
解释：和恰好为 6 ，已经能被 3 整除了。所以我们不需要移除任何元素。
```

**示例 4：**

```
输入：nums = [1,2,3], p = 7
输出：-1
解释：没有任何方案使得移除子数组后剩余元素的和被 7 整除。
```

**示例 5：**

```
输入：nums = [1000000000,1000000000,1000000000], p = 3
输出：0
```



**提示：**

- `1 <= nums.length <= 105`
- `1 <= nums[i] <= 109`
- `1 <= p <= 109`

```cpp
class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        long long sum = 0;//注意数据范围
        for (int i =  0;i<nums.size();i++){
            sum += nums[i];
        }
        int key = sum % p;
        int minlen = nums.size();
        //key : 前缀和%p的余数
        //value：最晚出现的位置
        unordered_map<int, int> ump;
        ump[0] = -1;
        if (key == 0) return 0;//整个数组本身就满足条件，不需要删除任何子数组
        sum = 0;
        for (int i = 0;i<nums.size();i++){
            sum += nums[i];
            int x = (sum + p - key) % p;//sum % p是当前0~i的余数，key是整体余数，找前面余数为x的位置，从x+1到i的区间的余数就是key
            if (ump.count(x)){
                minlen = min(minlen, i - ump[x]);
            }
            ump[sum % p] = i;
        }
        return minlen == nums.size() ? -1 : minlen;
    }
};
```

### [T5 每个元音包含偶数次的最长子字符串 leetcode N0.1371](https://leetcode.cn/problems/find-the-longest-substring-containing-vowels-in-even-counts/description/)

给你一个字符串 `s` ，请你返回满足以下条件的最长子字符串的长度：每个元音字母，即 'a'，'e'，'i'，'o'，'u' ，在子字符串中都恰好出现了偶数次。



**示例 1：**

```
输入：s = "eleetminicoworoep"
输出：13
解释：最长子字符串是 "leetminicowor" ，它包含 e，i，o 各 2 个，以及 0 个 a，u 。
```

**示例 2：**

```
输入：s = "leetcodeisgreat"
输出：5
解释：最长子字符串是 "leetc" ，其中包含 2 个 e 。
```

**示例 3：**

```
输入：s = "bcbcbc"
输出：6
解释：这个示例中，字符串 "bcbcbc" 本身就是最长的，因为所有的元音 a，e，i，o，u 都出现了 0 次。
```



**提示：**

- `1 <= s.length <= 5 x 10^5`
- `s` 只包含小写英文字母。

```cpp
//位运算逻辑
class Solution {
public:
    int get_pos(char c){
        switch(c){
            case 'a': return 0;
            case 'e': return 1;
            case 'i': return 2;
            case 'o': return 3;
            case 'u': return 4;
            default: return -1;
        }
    }
    int findTheLongestSubstring(string s) {
        int n = s.size();
        vector<int> status(32, -2);//-2表示之前这个状态没出现过
        status[0] = -1;
        int ans = 0;
        for (int i = 0, state = 0, m;i<n;i++){
            //当前字符不是元音，state不变
            //当前字符是元音，修改相应的状态
            m = get_pos(s[i]);
            if (m != -1){
                state ^= 1 << m;
            }
            //state变成0……i字符串上的aeiou的奇偶性
            //同样的状态，之前最早出现在哪
            if(status[state] != -2){
                ans = max(ans, i - status[state]);
            }
            else{
                status[state] = i;
            }
        }
        return ans;
    }
};
```
