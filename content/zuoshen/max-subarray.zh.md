# 子数组最大累加和问题与扩展

## leetcode 2560. 打家劫舍 IV

[原题](https://leetcode.cn/problems/house-robber-iv/description/)

沿街有一排连续的房屋。每间房屋内都藏有一定的现金。现在有一位小偷计划从这些房屋中窃取现金。

由于相邻的房屋装有相互连通的防盗系统，所以小偷 **不会窃取相邻的房屋** 。

小偷的 **窃取能力** 定义为他在窃取过程中能从单间房屋中窃取的 **最大金额** 。

给你一个整数数组 `nums` 表示每间房屋存放的现金金额。形式上，从左起第 `i` 间房屋中放有 `nums[i]` 美元。

另给你一个整数 `k` ，表示窃贼将会窃取的 **最少** 房屋数。小偷总能窃取至少 `k` 间房屋。

返回小偷的 **最小** 窃取能力。



**示例 1：**

```
输入：nums = [2,3,5,9], k = 2
输出：5
解释：
小偷窃取至少 2 间房屋，共有 3 种方式：
- 窃取下标 0 和 2 处的房屋，窃取能力为 max(nums[0], nums[2]) = 5 。
- 窃取下标 0 和 3 处的房屋，窃取能力为 max(nums[0], nums[3]) = 9 。
- 窃取下标 1 和 3 处的房屋，窃取能力为 max(nums[1], nums[3]) = 9 。
因此，返回 min(5, 9, 9) = 5 。
```

**示例 2：**

```
输入：nums = [2,7,9,3,1], k = 2
输出：2
解释：共有 7 种窃取方式。窃取能力最小的情况所对应的方式是窃取下标 0 和 4 处的房屋。返回 max(nums[0], nums[4]) = 2 。
```



**提示：**

- `1 <= nums.length <= 105`
- `1 <= nums[i] <= 109`
- `1 <= k <= (nums.length + 1)/2`

 ```cpp
 class Solution {
 public:
    bool check(vector<int> & nums, int k, int ability){
        // dp[i] : 前i个房屋最多能偷多少个
        // return : dp[n-1]
        int n = nums.size();
        vector<int> dp(n, 0);
        dp[0] = nums[0] <= ability ? 1 : 0;
         if(n == 1){
             return dp[0] >= k;
         }
        if(!(nums[0] > ability && nums[1] > ability)){
             dp[1] = 1;
         }
        for (int i = 2; i<n;i++){
            if (nums[i] <= ability){
                dp[i] = max(1 + dp[i-2], dp[i-1]);
            }
            else{
                dp[i] = dp[i-1];
            }
        }
        return k <= dp[n-1];
    }
     int minCapability(vector<int>& nums, int k) {
         int l = INT_MAX, r = INT_MIN, mid, ans = -1;
         int n = nums.size();
         for (int i = 0; i<n;i++){
            l = min(l, nums[i]);
            r = max(r, nums[i]);
        }
        while (l <= r){
            mid = l + (r - l) / 2;
            if (check(nums, k, mid)){
                ans = mid;
                r = mid - 1;
            }
            else{
                l = mid + 1;
            }
        }
        return ans;
     }
 };
 ```

## leetcode 17.24. 最大子矩阵

[原题](https://leetcode.cn/problems/max-submatrix-lcci/description/)

给定一个正整数、负整数和 0 组成的 N × M 矩阵，编写代码找出元素总和最大的子矩阵。

返回一个数组 `[r1, c1, r2, c2]`，其中 `r1`, `c1` 分别代表子矩阵左上角的行号和列号，`r2`, `c2` 分别代表右下角的行号和列号。若有多个满足条件的子矩阵，返回任意一个均可。

**注意：**本题相对书上原题稍作改动

**示例：**

```
输入：
[
   [-1,0],
   [0,-1]
]
输出：[0,1,0,1]
解释：输入中标粗的元素即为输出所表示的矩阵
```



**说明：**

- `1 <= matrix.length, matrix[0].length <= 200`

```cpp
class Solution {
public:
    vector<int> getMaxMatrix(vector<vector<int>>& matrix) {
        int r1 = 0, c1 = 0, r2 = 0, c2 = 0;
		int max = INT_MIN;
		int n = matrix.size();
		int m = matrix[0].size();
		vector<int> nums(m, 0);
		for (int up = 0; up<n;up++){
			fill(nums.begin(), nums.end(), 0);
			for (int down = up; down<n;down++){
				for(int l = 0, r = 0, pre = INT_MIN; r < m; r++){
					nums[r] += matrix[down][r];
					if (pre >= 0){
						pre += nums[r];
					}
					else{
						pre = nums[r];
						l = r;
					}
					if (pre > max){
						max = pre;
						r1 = up;
						c1 = l;
						r2 = down;
						c2 = r;
					}
				}
			}

		}
		vector<int> ans(4, 0);
		ans[0] = r1;
		ans[1] = c1;
		ans[2] = r2;
		ans[3] = c2;
		return ans;
    }
};
```
