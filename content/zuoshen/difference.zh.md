# 差分

## 1.一维差分和等差数列差分

注意:差分数组不支持**边操作边查询**,树状数组才支持

[l, r] + v

[l] += v;

[r+1] -= v;

### [T1 航班预定统计 leetcode No.1109](https://leetcode.cn/problems/corporate-flight-bookings/description/)

这里有 `n` 个航班，它们分别从 `1` 到 `n` 进行编号。

有一份航班预订表 `bookings` ，表中第 `i` 条预订记录 `bookings[i] = [firsti, lasti, seatsi]` 意味着在从 `firsti` 到 `lasti` （**包含** `firsti` 和 `lasti` ）的 **每个航班** 上预订了 `seatsi` 个座位。

请你返回一个长度为 `n` 的数组 `answer`，里面的元素是每个航班预定的座位总数。



**示例 1：**

```
输入：bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5
输出：[10,55,45,25,25]
解释：
航班编号        1   2   3   4   5
预订记录 1 ：   10  10
预订记录 2 ：       20  20
预订记录 3 ：       25  25  25  25
总座位数：      10  55  45  25  25
因此，answer = [10,55,45,25,25]
```

**示例 2：**

```
输入：bookings = [[1,2,10],[2,2,15]], n = 2
输出：[10,25]
解释：
航班编号        1   2
预订记录 1 ：   10  10
预订记录 2 ：       15
总座位数：      10  25
因此，answer = [10,25]
```



**提示：**

- `1 <= n <= 2 * 104`
- `1 <= bookings.length <= 2 * 104`
- `bookings[i].length == 3`
- `1 <= firsti <= lasti <= n`
- `1 <= seatsi <= 104`

```cpp
class Solution {
public:
    vector<int> corpFlightBookings(vector<vector<int>>& bookings, int n) {
        vector<int> ans(n+1, 0);
        //差分核心
        for (const auto & book : bookings){
            ans[book[0] - 1] += book[2];
            ans[book[1]] -= book[2];
        }
        vector<int> res(n, 0);
        res[0] = ans[0];
        //前缀和
        for (int i = 0;i<n-1;i++){
            res[i+1] = res[i] + ans[i+1];
        }
        return res;
    }
};
```

### [T2 三步必杀 luogu P4231](https://www.luogu.com.cn/problem/P4231)

板子题,理解等差数列差分的两步走:

1. 每次都调用set方法
2. 所有操作完成后在arr上生成两遍前缀和

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
ll n, m;
ll l, r, s, e, d;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    vector<ll> a(n+3, 0);
    for(int i = 0;i<m;i++){
        cin >> l >> r >> s >> e;
        d = (e - s) / (r - l);
        //从1开始的下标
        a[l] += s;
        a[l+1] += -s + d;
        a[r+1] -= d + e;
        a[r+2] += e;
    }
    for(int i = 1; i <= n; i++){
        a[i] = a[i-1] + a[i];
    }
    ll ans = 0;
    ll res = 0;
    for(int i = 1; i <= n; i++){
        a[i] = a[i-1] + a[i];
        ans ^= a[i];
        res = max(res, a[i]);
    }
    cout << ans << " " << res;
    return 0;
}
```

### [T3 Lycanthropy luogu P5026](https://www.luogu.com.cn/problem/P5026)

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1000001;
const int OFFSET = 30001;
using ll = long long;
ll a[OFFSET + MAXN + OFFSET] = {0};
int n, m;
void change(int l, int r, int s, int e, int d){
    a[OFFSET + l] += s;
    a[OFFSET + l + 1] += -s + d;
    a[OFFSET + r + 1] -= d + e;
    a[OFFSET + r + 2] += e;
    return;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    int v, x;
    for (int i = 0;i<n;i++){
        cin >> v >> x;
        change(x - 3 * v + 1, x - 2 * v, 1, v, 1);
        change(x - 2 * v + 1, x, v - 1, -v, -1);
        change(x + 1, x + 2 * v, -v + 1, v, 1);
        change(x + 2 * v + 1, x + 3 * v - 1, v - 1, 1, -1);
    }
    for (int i = 1; i<= m + OFFSET; i++){
        a[i] += a[i-1];
    }
    for (int i = 1; i<= m + OFFSET; i++){
        a[i] += a[i-1];
    }
    for (int i = OFFSET + 1; i <= m + OFFSET; i++){
        cout << a[i] << ' ';
    }
    return 0;
}
```

## 2.二维前缀和,二维差分,离散化技巧

### 二维前缀和

目的是预处理出一个结构,以后每次查询二维数组任何范围上的累加和都是O(1)的操作

1. 根据原始状况,生成二维前缀和数组sum(左 + 上 - 左上 + 自己)
* sum[ i ]  [ j ]:代表左上角(0, 0)到右下角(i, j)这个范围的累加和
* sum[ i ]  [ j ] += sum[ i ]  [ j - 1] + sum[ i - 1]  [ j ] - sum[ i - 1]  [ j - 1];
2. 查询左上角(a, b)到右下角(c, d)这个范围的累加和(自己 - (左 + 上 - 左上))
* sum[ c ]  [ d ]  -= sum[ c ]  [ b  -  1] + sum[ a - 1 ]  [ d ]  - sum[a-1]  [b-1]
3.
