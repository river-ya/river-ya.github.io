# 二分查找

## 1.二分搜索

时间复杂度： $ O(\log n) $

### 1.1 在有序数组中查找某个target值是否存在

**注意这里的有序是指从小到大**

```cpp
bool is_existence(vector<int> & a, int target){
    if (a.empty()) return false;
    int l = 0, r = a.size() - 1, mid = 0;// [l, r]左闭右闭
    while(l <= r){
        mid = l + (r - l) / 2;
        if (a[mid] == target) return true;
        else if(a[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    return false;
}
```

### 1.2 在有序数组中找>=target或>target的最左位置

```cpp
int binary_find_left(vector<int> & a, int target){
    int l = 0, r = a.size() - 1, mid = 0;
    int ans = -1;
    while(l <= r){
        mid = l + (r - l) / 2;
        if (a[mid] >= target){//找到符合条件的，更新答案(如果找大于target的最左位置则改成大于)
            ans = mid;//记忆一个答案往左二分
            r = mid - 1;
        }
        else{//没有找到符合条件的，不更新答案
            l = mid + 1;//不记忆答案往右二分
        }
    }
    return ans;//如果返回-1则表明没有找到大于等于target的数字
}
```

### 1.3 在有序数组中找<=target或<target的最右位置

```cpp
int binary_find_right(vector<int> & a, int target){
    int l = 0, r = a.size() - 1, mid = 0;
    int ans = -1;
    while(l <= r){
        mid = l + (r - l) / 2;
        if (a[mid] <= target){//找到符合条件的，更新答案(如果找小于target的最右位置则改成小于)
            ans = mid;//记忆一个答案往右二分
            l = mid + 1;
        }
        else{//没有找到符合条件的，不更新答案
            r = mid - 1;//不记忆答案往左二分
        }
    }
    return ans;//如果返回-1则表明没有找到小于等于target的数字
}
```

### 1.4 二分搜索不一定发生在有序数组中

[寻找峰值 Leetcode No.162](https://leetcode.cn/problems/find-peak-element/description/)
先看题目，再看题解（
我们只需要找**任何一个峰值**即可
默认两边是超小值，且每个相邻元素不等

```cpp
int find_summit(vector<int> & a){
    int n = a.size();
    if (n == 1) return 0;
    //单独验证0位置是不是峰值点
    if (a[0] > a[1]) return 0;
    //单独验证n-1位置是不是峰值点
    if (a[n-1] > a[n-2]) return n-1;
    //[1, n-2] 一定有峰值点（比较类似于罗尔定理）
    int l = 1, r = n - 2, mid = 0;
    int ans = -1;
    while(l <= r){
        mid = l + (r - l)/ 2;
        if(a[mid-1] > a[mid]){//某侧必有就可以二分了
            r = mid - 1;
        }
        else if (a[mid] < a[mid+1]){
            l = mid + 1;
        }
        else{//mid是峰值
            ans = mid;
            break;
        }
    }
    return ans;
}
```

### 1.5 对数器

实际上跟二分没啥关系，只是一个验证的手段，在入门阶段是很必要学习的
遇到一个**巨大的数据集**然后WA了，但是他不给你错误的测试集或者测试集特别大，根本没法debug，这时就要用对数器了
面对一个有输入和输出的问题，实际上我们一般会有两种思路，一种**纯暴力**，一种是你**想象中的最优解**（但是否完全正确你并不清楚）
我们可以自己生成出一个随机数据集，你既可以**控制数据长度**也能**控制数据值的范围**（保证测试集较小，暴力不会太耗时间）
经过多次测试，如果你的暴力解ans1和最优解ans2的答案总是一样的
如果发现ans1和ans2的结果不一样，那么我们可以打印出我们的测试集（保证短），再打印出所有的中间结果，步步排错
如果小数据结果一样，那么可以适当跑一跑长数据，如果也没问题，那基本应该没啥问题了

tips： 尤其在验证**贪心**、**观察规律**的题目中很有用

```cpp
#include <bits/stdc++.h>
using namespace std;
// ================= 暴力解（保证正确） =================
int brute(vector<int>& a) {
    int res = 0;
    for (int i = 0; i < a.size(); i++) {
        for (int j = i; j < a.size(); j++) {
            res += a[j]; // 举例：区间和
        }
    }
    return res;
}
// ================= 你的算法 =================
int fast(vector<int>& a) {
    int res = 0;
    int prefix = 0;
    for (int x : a) {
        prefix += x;
        res += prefix;
    }
    return res;
}
// ================= 随机数据生成 =================
vector<int> generate() {
    vector<int> a;
    int n = rand() % 10 + 1; // 小范围！
    for (int i = 0; i < n; i++) {
        a.push_back(rand() % 20 - 10); // [-10,10]
    }
    return a;
}

// ================= 打印数据（调试用） =================
void print(vector<int>& a) {
    for (int x : a) cout << x << " ";
    cout << "\n";
}

// ================= 主函数 =================
int main() {
    srand(time(0)); // 随机种子

    for (int t = 1; t <= 100000; t++) {
        auto a = generate();

        int ans1 = brute(a);
        int ans2 = fast(a);

        if (ans1 != ans2) {
            cout << " 出错！\n";
            cout << "数据：";
            print(a);

            cout << "brute = " << ans1 << "\n";
            cout << "fast  = " << ans2 << "\n";
            return 0;
        }
    }

    cout << " 全部通过！\n";
    return 0;
}
```
