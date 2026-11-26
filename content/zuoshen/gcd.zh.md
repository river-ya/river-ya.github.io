# 最大公约数和最小公倍数

辗转相除法（欧几里得方法）

时间复杂度 O((log a) ^ 3)

```cpp
int gcd(int a, int b){
	return b == 0 ? a : gcd(b, a % b);
}
int lcm(int a, int b){
    return a / gcd(a, b) * b;//防止溢出
}
```

## leetcode No.878 第N个神奇的数字

[原题](https://leetcode.cn/problems/nth-magical-number/description/)

一个正整数如果能被 `a` 或 `b` 整除，那么它是神奇的。

给定三个整数 `n` , `a` , `b` ，返回第 `n` 个神奇的数字。因为答案可能很大，所以返回答案 **对** `109 + 7` **取模** 后的值。



**示例 1：**

```
输入：n = 1, a = 2, b = 3
输出：2
```

**示例 2：**

```
输入：n = 4, a = 2, b = 3
输出：6
```



**提示：**

- `1 <= n <= 109`
- `2 <= a, b <= 4 * 104`

```cpp
//二分答案
using ll = long long;
#define mod 1000000007
class Solution {
public:
    ll GCD(ll a, ll b){
        return b == 0 ? a : GCD(b, a % b);
    }
    ll lcm(ll a, ll b){
        return a / GCD(a, b) * b;
    }
    int check(ll x, ll a ,ll b){
        int cnt = x / a + x / b - x / lcm(a, b); //注意不是a * b，而是找到最小公倍数
        return cnt;
    }
    int nthMagicalNumber(int n, int a, int b) {
        ll l = 0, r = (ll)min(a, b) * (ll)n, mid = 0, ans = -1;
        while (l <= r){
            mid = l + (r - l) / 2;
            ll tmp = check(mid, a, b);
            //一定是>=，因为要找的是满足第n个数字的最小值，就比如a = 2, b = 3时找第三小的数字，mid = 6/7都是满足题意的，但是要取6
            if (tmp >= n){
                ans = mid;
                r = mid - 1;
            }
            else{
                l = mid + 1;
            }
        }
        return (ans % mod);
    }
};
```
# 同余原理

(a % mod + b % mod) % mod = (a+b) % mod

(a % mod * b % mod) % mod = (a * b) % mod

((a % mod - b % mod) + mod) % mod = (a - b) % mod

除法同余需要求逆元
