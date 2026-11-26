## 2.二分答案

二分答案法：（有点**逆向思维**的感觉，即验证答案是否正确）

* 估计**最终答案可能的范围**是什么,可以很粗略（说白了就是l和r的初始取值）
* 分析**问题的答案和给定条件的单调性**，大部分只用到**自然智慧**（大胆猜，如果没有单调性果断放弃二分答案）
* 建立一个**check函数**，当答案固定的情况下，判断给定的条件是否达标（check函数复杂度尽可能的低，**最坏O(n)**）
* 达标后记录答案去某侧二分，不断不断的二分，最终找到答案

### T1 爱吃香蕉的珂珂 leetcode No.875

[原题](https://leetcode.cn/problems/koko-eating-bananas/description/)

珂珂喜欢吃香蕉。这里有 n 堆香蕉，第 i 堆中有 **piles[i]** 根香蕉。警卫已经离开了，将在 h 小时后回来。

珂珂可以决定她吃香蕉的速度 k （单位：根/小时）。每个小时，她将会选择一堆香蕉，从中吃掉 k 根。如果这堆香蕉少于 k 根，她将吃掉这堆的所有香蕉，然后这一小时内不会再吃更多的香蕉。

珂珂喜欢慢慢吃，但仍然想在警卫回来前吃掉所有的香蕉。

返回她可以在 h 小时内吃掉所有香蕉的最小速度 k（k 为整数）。
示例 1：

输入：piles = [3,6,7,11], h = 8
输出：4
示例 2：

输入：piles = [30,11,23,4,20], h = 5
输出：30
示例 3：

输入：piles = [30,11,23,4,20], h = 6
输出：23

提示：

1 <= piles.length <= <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mn>10</mn><mn>4</mn></msup></mrow></math>
piles.length <= h <= <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mn>10</mn><mn>9</mn></msup></mrow></math>
1 <= piles[i] <= <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mn>10</mn><mn>9</mn></msup></mrow></math>

```cpp
//1.确定范围：l = 0, r = max(piles[i])
//求解的问题是：吃掉所有香蕉的最小速度k，那么我可以找出所有可能满足条件的spead然后选出最小的
//2.单调性：spead越快，越可能吃完（满足条件） ，可以往左二分
bool check(vector<int> & piles, int k, int h){
        long long  cnt = 0;
        for (int i = 0;i<piles.size();i++){
            cnt += (piles[i] + k - 1)/ k;//a/b向上取整==(a+b-1)/b向下取整
        }
        if(cnt <= h) return true;
        return false;
    }
    int minEatingSpeed(vector<int>& piles, int h) {
        int max_val = -1;
        int n = piles.size();
        for (int i = 0;i<n;i++){
            if(piles[i] > max_val) max_val = piles[i];
        }
        //单调性满足：k越大所用时间一定不会变多
        int l = 1, r = max_val, mid = 0;//注意l是从1开始，而不是min_val
        int ans = -1;
        while(l <= r){
            mid = l + (r-l)/ 2;
            if(check(piles,mid,h)){//达标左侧二分并记录答案
                ans = mid;
                r = mid - 1;
            }
            else{
                l = mid + 1;
            }
        }
        return ans;
    }
```

时间复杂度：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>O</mi><mo stretchy="false">&#x00028;</mo><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">&#x00028;</mo><mi>m</mi><mi>a</mi><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002A;</mo><mi>n</mi><mo stretchy="false">&#x00029;</mo></mrow></math>
额外空间复杂度： O(1)

### T2 分割数组的最大值(画匠问题) leetcode No.410

[原题](https://leetcode.cn/problems/split-array-largest-sum/)

*这道题实际上可以用动态规划（），但此处用二分答案就够用了*
给定一个非负整数数组 nums 和一个整数 k ，你需要将这个数组分成 k 个非空的连续子数组，使得这 k 个子数组各自和的最大值 最小。

返回分割后最小的和的最大值。

子数组 是数组中连续的部分。

示例 1：

输入：nums = [7,2,5,10,8], k = 2
输出：18
解释：
一共有四种方法将 nums 分割为 2 个子数组。
其中最好的方式是将其分为 [7,2,5] 和 [10,8] 。
因为此时这两个子数组各自的和的最大值为18，在所有情况中最小。
示例 2：

输入：nums = [1,2,3,4,5], k = 2
输出：9
示例 3：

输入：nums = [1,4,4], k = 3
输出：4

提示：

1 <= nums.length <= 1000
0 <= nums[i] <= <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mn>10</mn><mn>6</mn></msup></mrow></math>
1 <= k <= min(50, nums.length)

```cpp
// 1.确定范围： l = 0, r = sum
// 2.单调性：我猜出的mid越大，分割成的数组数量一定越多，那么就更易满足条件
bool check(vector<int> & nums, int k, int max_val){
        int cnt = 0;
        int idx = 0;
        int sum = 0;
        for (int i = 0;i<nums.size();i++){
            if (nums[i] > max_val) return false;//最容易忽略的点，如果单点的值超过max-val则返回false（如果忽略此点则需要改动l的初始值为max）
            sum += nums[i];
            if(sum > max_val){
                sum = nums[i];
                cnt++;
            }
        }
        if(sum > 0) cnt++;
        return cnt<=k;
    }
    int splitArray(vector<int>& nums, int k) {
        int len = nums.size();
        int l = 0, r = 0, m = 0, ans = 0;
        for(int i = 0;i<len;i++){
            r += nums[i];//区间[0,整个数组的累加和]
        }
        //单调性：max越大表示我越可能成立，条件越宽
        while(l <= r){
            m = l + (r - l)/ 2;
            if (check(nums,k,m)){
                ans = m;
                r = m - 1;
            }
            else{
                l = m + 1;
            }
        }
        return ans;
    }
```

时间复杂度：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>O</mi><mo stretchy="false">&#x00028;</mo><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">&#x00028;</mo><mi>m</mi><mi>a</mi><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002A;</mo><mi>n</mi><mo stretchy="false">&#x00029;</mo></mrow></math>
额外空间复杂度： O(1)

### T3 机器人跳跃问题 newcode REAL254

[原题](https://www.nowcoder.com/practice/7037a3d57bbd4336856b8e16a9cafd71)

机器人正在玩一个古老的基于DOS的游戏。游戏中有N+1座建筑——从0到N编号，从左到右排列。编号为0的建筑高度为0个单位，编号为i的建筑的高度为H(i)个单位。

起初， 机器人在编号为0的建筑处。每一步，它跳到下一个（右边）建筑。假设机器人在第k个建筑，且它现在的能量值是E, 下一步它将跳到第个k+1建筑。它将会得到或者失去正比于与H(k+1)与E之差的能量。如果 H(k+1) > E 那么机器人就失去 H(k+1) - E 的能量值，否则它将得到 E - H(k+1) 的能量值。

游戏目标是到达第个N建筑，在这个过程中，能量值不能为负数个单位。现在的问题是机器人以多少能量值开始游戏，才可以保证成功完成游戏？
输入描述：
第一行输入，表示一共有 N 组数据.

第二个是 N 个空格分隔的整数，H1, H2, H3, ..., Hn 代表建筑物的高度
输出描述：
输出一个单独的数表示完成游戏所需的最少单位的初始能量
示例1
输入：
5
3 4 3 2 4

输出：
4

示例2
输入：
3
4 4 4

输出：
4

示例3
输入：
3
1 6 4

输出：
3

备注：
数据约束：
1 <= N <= 10^5
1 <= H(i) <= 10^5

```cpp
#include <bits/stdc++.h>
using namespace std;
int n;
vector<int> h;
bool check(int energy,int max){
    for (int i = 0;i<n;i++){
        if (energy < 0) return false;
        if (energy > max) return true;//剪枝，防止溢出，太阴了
        //一旦能量超过高度最大值，那么后续能量增长可能会很恐怖
        if (h[i] > energy) energy -= (h[i]- energy);
        else energy += (energy - h[i]);
    }
    if (energy < 0) return false;
    return true;
}
int main() {
    cin >> n;
    h.resize(n);
    for(int i = 0;i<n;i++){
        cin >> h[i];
    }
    int max = *max_element(h.begin(), h.end());
    int l = 0, r =max, mid = 0, ans = -1;
    //不要认为l初始值是h[0]，因为可以通过减少能量达到h[0],所以初始值设成0或者h[0] / 2
    //单调性：能量越大越有可能可以到达最后的塔
    while(l <= r){
        mid = l + (r - l) /2;
        if (check(mid,max)){
            ans = mid;
            r = mid - 1;
        }
        else{
            l = mid + 1;
        }
    }
    cout << ans;
    return 0;
}
```

时间复杂度：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>O</mi><mo stretchy="false">&#x00028;</mo><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">&#x00028;</mo><mi>m</mi><mi>a</mi><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002A;</mo><mi>n</mi><mo stretchy="false">&#x00029;</mo></mrow></math>
额外空间复杂度： O(1)

### T4 找出第K小的数对距离 leetcode No.719

[原题](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/description/)

数对 (a,b) 由整数 a 和 b 组成，其数对距离定义为 a 和 b 的绝对差值。

给你一个整数数组 nums 和一个整数 k ，数对由 nums[i] 和 nums[j] 组成且满足 0 <= i < j < nums.length 。返回 所有数对距离中 第 k 小的数对距离。

示例 1：

输入：nums = [1,3,1], k = 1
输出：0
解释：数对和对应的距离如下：
(1,3) -> 2
(1,1) -> 0
(3,1) -> 2
距离第 1 小的数对是 (1,1) ，距离为 0 。
示例 2：

输入：nums = [1,1,1], k = 2
输出：0
示例 3：

输入：nums = [1,6,1], k = 3
输出：5

提示：

n == nums.length
2 <= n <= <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mn>10</mn><mn>4</mn></msup></mrow></math>
0 <= nums[i] <= <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mn>10</mn><mn>6</mn></msup></mrow></math>
1 <= k <= n * (n - 1) / 2

```cpp
//注意是非去重
    bool check(vector<int> & nums,int val, int k){
        //滑动窗口
        int ans = 0;
        int l = 0, r = 0;
        while(l < nums.size()){
            while(r+1<nums.size() && nums[r+1] <= nums[l] + val){
                r++;
            }
            ans += r - l;
            l++;
        }
        return ans>=k;
    }
    int smallestDistancePair(vector<int>& nums, int k) {
        int n = nums.size();
        sort(nums.begin(), nums.end());//为了check函数的窗口
        int ans = 0;
        int l = 0, r = nums[n-1] - nums[0], mid = 0;
        //单调性：距离小于等于mid的数对如果超过k，比mid数大的阈值对应的数对应该也超过k，即右侧全部满足，应该左侧二分
        while(l<=r){
            mid = l + (r - l) / 2;
            if (check(nums, mid, k)){
                ans = mid;
                r = mid - 1;
            }
            else{
                l = mid + 1;
            }
        }
        return ans;
    }
```

时间复杂度：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>O</mi><mo stretchy="false">&#x00028;</mo><mi>n</mi><mo>&#x0002A;</mo><mi>log</mi><mi>n</mi><mo>&#x0002B;</mo><mi>n</mi><mo>&#x0002A;</mo><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">&#x00028;</mo><mi>m</mi><mi>a</mi><mi>x</mi><mo>&#x02212;</mo><mi>m</mi><mi>i</mi><mi>n</mi><mo stretchy="false">&#x00029;</mo><mo stretchy="false">&#x00029;</mo></mrow></math>
额外空间复杂度： O(1)

### T5 同时运行N台电脑的最长时间 leetcode No.2141

[原题](https://leetcode.cn/problems/maximum-running-time-of-n-computers/description/)

你有 n 台电脑。给你整数 n 和一个下标从 0 开始的整数数组 batteries ，其中第 i 个电池可以让一台电脑 运行 batteries[i] 分钟。你想使用这些电池让 全部 n 台电脑 同时 运行。

一开始，你可以给每台电脑连接 至多一个电池 。然后在任意整数时刻，你都可以将一台电脑与它的电池断开连接，并连接另一个电池，你可以进行这个操作 任意次 。新连接的电池可以是一个全新的电池，也可以是别的电脑用过的电池。断开连接和连接新的电池不会花费任何时间。

注意，你不能给电池充电。

请你返回你可以让 n 台电脑同时运行的 最长 分钟数。

示例 1：

输入：n = 2, batteries = [3,3,3]
输出：4
解释：
一开始，将第一台电脑与电池 0 连接，第二台电脑与电池 1 连接。
2 分钟后，将第二台电脑与电池 1 断开连接，并连接电池 2 。注意，电池 0 还可以供电 1 分钟。
在第 3 分钟结尾，你需要将第一台电脑与电池 0 断开连接，然后连接电池 1 。
在第 4 分钟结尾，电池 1 也被耗尽，第一台电脑无法继续运行。
我们最多能同时让两台电脑同时运行 4 分钟，所以我们返回 4 。
示例 2：

输入：n = 2, batteries = [1,1,1,1]
输出：2
解释：
一开始，将第一台电脑与电池 0 连接，第二台电脑与电池 2 连接。
一分钟后，电池 0 和电池 2 同时耗尽，所以你需要将它们断开连接，并将电池 1 和第一台电脑连接，电池 3 和第二台电脑连接。
1 分钟后，电池 1 和电池 3 也耗尽了，所以两台电脑都无法继续运行。
我们最多能让两台电脑同时运行 2 分钟，所以我们返回 2 。

提示：

1 <= n <= batteries.length <= 10^5
1 <= batteries[i] <= 10^9

```cpp
//本题涉及碎片电池的问题，如果每个电池的电量都小于等于要求的分钟数，那么称这个电池为碎片电池
//结论： 如果电池全是碎片电池，那么他们的sum如果大于等于要求的分钟数*电脑数，那么一定可以满足
//反之，如果sum小于要求的分钟数*电脑数，那么一定不满足
//证明：电池可以按照顺序进行分配，由于电池的电量小于等于要求的分钟数，可以确保不会有任何的浪费，那么一定能满足
//如果有单个电池超过了要求的分钟数，那么剩下的电池电量一定是被浪费的，因为不能同时使用两个电池，那么可以把超过要求的分钟数的电池抵消一个电脑或者将其限制成要求的分钟数
    bool check(vector<int> & nums, long long val,int n){
        long long sum = 0;
        for(auto num : nums){
            if(num > val){
                n--;
            }
            else{
                //是碎片电池
                sum += num;
            }
        }
        if (sum >= n * val){
            return true;
        }
        return false;
    }
    long long maxRunTime(int n, vector<int>& batteries) {
        long long len = batteries.size();
        long long l = 0, r = 0;
        for (int i = 0;i<len;i++){
            r += batteries[i];
        }
        long long mid = 0, ans = -1;
        //单调性：撑x分钟比撑x+1分钟更简单
        while(l <= r){
            mid = l + (r - l) / 2;
            if (check(batteries,mid, n)){
                ans = mid;
                l = mid + 1;
            }
            else{
                r = mid - 1;
            }
        }
        return ans;
    }
//可以优化 二分答案+贪心


cpp
    bool check(vector<int> & nums, long long val,int n){
        long long sum = 0;
        for(auto num : nums){
            if(num > val){
                n--;
            }
            else{
                sum += num;
            }
        }
        if (sum >= n * val){
            return true;
        }
        return false;
    }
    long long maxRunTime(int n, vector<int>& batteries) {
        long long len = batteries.size();
        long long l = 0, r = 0;
        long long max = -1;
        for (int i = 0;i<len;i++){
            r += batteries[i];
            if (batteries[i] > max){
                max = batteries[i];
            }
        }
        long long mid = 0, ans = -1;
        //单调性：撑x分钟比撑x+1分钟更简单
        //所有的电池的最大电量是max
        //如果此时sum>=max*num
        //说明：最终的供电时间一定大于等于max，那么所有电池都是碎片电池
        //则答案为 sum/num
        if(r >= max * n){
            return r/n;
        }
        while(l <= r){
            mid = l + (r - l) / 2;
            if (check(batteries,mid, n)){
                ans = mid;
                l = mid + 1;
            }
            else{
                r = mid - 1;
            }
        }
        return ans;
    }
```

时间复杂度：<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>O</mi><mo stretchy="false">&#x00028;</mo><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">&#x00028;</mo><mi>s</mi><mi>u</mi><mi>m</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002A;</mo><mi>n</mi><mo stretchy="false">&#x00029;</mo></mrow></math>
额外空间复杂度： O(1)

### T6 计算等位时间 google 面试

给定一个数组arr长度为n，表示n个服务员每个人服务一个人的时间
给定一个正数m，表示有m个人等位，如果你是刚来的人，每个客人遵循有空位就上的原则，请问你需要等多久？
假设m远远大于n，比如n <= 10^3,m <= 10^9,该怎么做是最优解？

读题最大的困惑是：该怎么选择服务员？
但实际上通过列举感受，**遵循有空位就上的原则，无论怎么选择服务员，轮到你的时间是固定的**

```cpp
"""
可以利用小根堆来做（醒的时间来排序）
假设服务arr数组为：  [1,3,5]
小根堆 ：  0,1                          0,3         0,5     1,1     2,1     3,1
          0,3                     ->   0,5      -> 1,1 ->  3,3  -> 3,3  -> 3,3 -> ……
          0,5                          1,1         3,3     5,5     5,5     5,5
"""
struct cmp{
    bool operator()(pair<int,int> a, pair<int,int> b){
        return a.first > b.first;//小顶堆
    }
};
//注意区分sort和优先队列的比较函数是逻辑相反的
//sort：cmp 决定“谁在前”（直接写bool cmp函数）
//pq：cmp 决定“谁更差”（cmp（a，b） == true ,那么表明a应该优先级更低，放在下面）（需要结构体或者叫类型的写法）
int waitingname(vector<int> & arr, int m){
    priority_queue<pair<int,int>, vector<pair<int,int>>, cmp> pque;//<醒来时间，服务一个客人需要多久>
    int n = arr.size();
    for (int i = 0;i<n;i++)
    {
        pque.push({0, arr[0]});
    }
    for (int i = 0;i<m;i++){
        pair<int,int> pr = pque.top();
        pque.pop();
        pr.first += pr.first + pr.second;
        pque.push(pr);
    }
    return pque.top().first;
}
//但是当m很大的时候会超时,只做验算，即对数器方法
//时间复杂度：O(m * log(n))
//额外空间复杂度：O(n)
cpp
//时间复杂度： O(log(min * m) * n)
//额外空间复杂度：O(1)
bool check(vector<int> & nums, int time, int m){
    //细节超多，不能走神！！！
    //首先要注意我们是要算接受服务的开始时间，而不是接受完服务的时间，所以比如time是8h，假如第一个服务员服务一个人的时间是2h，那么我们应该算有5个人可以在8h内接受服务（刚开头的也要算）
    long long cnt = 0;
    int n = nums.size();
    for (int i = 0;i<n;i++){
        cnt += nums[i] / time + 1;//必须加1
    }
    if (cnt >= m + 1)//必须把自己算进去
    {
        return true;
    }
    return false;
}
int waitingtime(vector<int> & arr, int m){
    int n = arr.size();
    int l = 0, r = *min_element(arr.begin(), arr.end()) * m, mid = 0, ans = -1;
    while(l <= r){
        //m是中点，表示一定要让服务员工作的时间，算出能够给多少客人服务
        mid = l + (r - l) / 2;
        if (check(arr, mid, m)){
            ans = mid;
            r = mid - 1;
        }
        else{
            l = mid + 1;
        }
    }
    return ans;
}
```

### T7 刀砍毒杀怪兽问题 真实大厂算法笔试题

怪兽的初始血量是一个整数hp，给出每一回合刀砍和毒杀的数值cuts和poisons
第i回合如果用刀砍，怪兽会在这回合直接损失cuts[i]的血，不再有后续效果
第i回合如果用毒杀，怪兽在这回合不会损失血量，但是之后每回合都损失poisons[i]的血量
并且你选择的所有毒杀效果在之后的回合中都会叠加
两个数组cuts，poisons，长度都是n，代表你一共可以进行n回合
每一回合你只能选择刀砍或者毒杀中的一个动作
如果你在n个回合中没有直接杀死怪兽，意味着你已经无法有新的行动了
但是如果怪兽如果有中毒效果的话，那么怪兽依然会不停扣血，直到血量耗尽的那回合死掉
返回至少需要多少回合怪兽会死掉
数据范围:
1 <= n <=10^5;
1 <= hp <=10^9;
1 <= cuts[i];
poisons[i] <= 10^9

```cpp
//时间复杂度：O(n * log(hp))
//额外空间复杂度：O(1)
bool check(vector<int> & cuts, vector<int> & poisons, int x, int hp){
    int len = min(cuts.size(),x);//因为x定的回合数可能超过n，必须取最小
    for (int i = 0;i<len;i++){
        //回合数确定，直接贪心选择局部最优
        int op = max(cuts[i], poisons[i] * (x - i));//比较刀伤和毒伤的累加伤害
        hp -= op;
        if (hp <= 0) return true;
    }
    return false;
}
int min_val(vector<int> & cuts, vector<int> & poisons, int n, int hp){
    int l = 1, r = hp, mid = 0, ans = -1;
    //单调性：回合数越多越容易打败怪兽
    while(l <= r){
        mid = l + (r - l) / 2;
        if (check(cuts, poisons, mid, hp)){
            ans = mid;
            r = mid - 1;
        }
        else{
            l = mid + 1;
        }
    }
    return ans;
}
```
