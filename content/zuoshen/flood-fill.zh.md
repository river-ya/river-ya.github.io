# 洪水填充

洪水填充是一种很简单的技巧，设置路径信息进行剪枝和统计，类似感染的过程

路径信息不撤销，看似暴力，但效率很高

## leetcode No.200 岛屿的数量

并查集里的一道题，但是洪水填充才是最优解

```cpp
class Solution {
public:
    void dfs(int i, int j, vector<vector<char>> & grid){
        if (i < 0 || i == grid.size() || j < 0 || j == grid[0].size() || grid[i][j] != '1'){
            return;
        }
        grid[i][j] = 0;
        dfs(i - 1, j, grid);
        dfs(i, j - 1, grid);
        dfs(i, j + 1, grid);
        dfs(i + 1, j, grid);
    }
    int numIslands(vector<vector<char>>& grid) {
        int n = grid.size();
        int m = grid[0].size();
        int cnt = 0;
        for (int i = 0;i<n;i++){
            for (int j = 0;j<m;j++){
                if (grid[i][j] == '1'){
                    dfs(i, j, grid);
                    cnt++;
                }
            }
        }
        return cnt;
    }

};
```

## leetcode No.130 被围绕的区域

[原题](https://leetcode.cn/problems/surrounded-regions/description/)

给你一个 `m x n` 的矩阵 `board` ，由若干字符 `'X'` 和 `'O'` 组成，**捕获** 所有 **被围绕的区域**：

- **连接：**一个单元格与水平或垂直方向上相邻的单元格连接。
- **区域：连接所有** `'O'` 的单元格来形成一个区域。
- **围绕：**如果一个区域中的所有 `'O'` 单元格都不在棋盘的边缘，则该区域被包围。这样的区域 **完全** 被 `'X'` 单元格包围。

通过 **原地** 将输入矩阵中的所有 `'O'` 替换为 `'X'` 来 **捕获被围绕的区域**。你不需要返回任何值。



**示例 1：**

**输入：**board = [['X','X','X','X'],['X','O','O','X'],['X','X','O','X'],['X','O','X','X']]

**输出：**[['X','X','X','X'],['X','X','X','X'],['X','X','X','X'],['X','O','X','X']]

**解释：**

[原题配图](https://pic.leetcode.cn/1718167191-XNjUTG-image.png)

在上图中，底部的区域没有被捕获，因为它在 board 的边缘并且不能被围绕。

**示例 2：**

**输入：**board = [['X']]

**输出：**[['X']]



**提示：**

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 200`
- `board[i][j]` 为 `'X'` 或 `'O'`

```cpp
class Solution {
public:
    void dfs(int i, int j, vector<vector<char>> & board){
        if (i < 0 || i == board.size() || j < 0 || j == board[0].size() || board[i][j] != 'O'){
            return;
        }
        board[i][j] = 'F';
        dfs(i, j - 1, board);
        dfs(i, j + 1, board);
        dfs(i - 1, j, board);
        dfs(i + 1, j, board);
    }
    void solve(vector<vector<char>>& board) {
        int n = board.size();
        int m = board[0].size();
        for (int i = 0; i < n; i++){
            if (board[i][0] == 'O'){         // 左边界
                dfs(i, 0, board);
            }
            if (board[i][m-1] == 'O'){       // 右边界
                dfs(i, m-1, board);
            }
        }
        for (int j = 0; j < m; j++){
            if (board[0][j] == 'O'){         // 上边界
                dfs(0, j, board);
            }
            if (board[n-1][j] == 'O'){       // 下边界
                dfs(n-1, j, board);
            }
        }
        for (int i = 0;i<n;i++){
            for(int j = 0; j < m;j++){
                if (board[i][j] == 'O'){
                    board[i][j] = 'X';
                }
                if (board[i][j] == 'F'){
                    board[i][j] = 'O';
                }
            }
        }
    }
};
```

## leetcode No.827 最大人工岛

[原题](https://leetcode.cn/problems/making-a-large-island/description/)

给你一个大小为 `n x n` 二进制矩阵 `grid` 。**最多** 只能将一格 `0` 变成 `1` 。

返回执行此操作后，`grid` 中最大的岛屿面积是多少？

**岛屿** 由一组上、下、左、右四个方向相连的 `1` 形成。



**示例 1:**

```
输入: grid = [[1, 0], [0, 1]]
输出: 3
解释: 将一格0变成1，最终连通两个小岛得到面积为 3 的岛屿。
```

**示例 2:**

```
输入: grid = [[1, 1], [1, 0]]
输出: 4
解释: 将一格0变成1，岛屿的面积扩大为 4。
```

**示例 3:**

```
输入: grid = [[1, 1], [1, 1]]
输出: 4
解释: 没有0可以让我们变成1，面积依然为 4。
```



**提示：**

- `n == grid.length`
- `n == grid[i].length`
- `1 <= n <= 500`
- `grid[i][j]` 为 `0` 或 `1`

```cpp
//并查集做法（和病毒那道题很像）
const int maxn = 250001;
class Solution {
public:
    int father[maxn];
    int setsize[maxn];
    int dirs[4][2] = {{-1, 0}, {0, -1}, {1, 0}, {0, 1}};
    void initSet(int n){
        for (int i = 0;i<n;i++){
            father[i] = i;
            setsize[i] = 1;
        }
    }
    int findSet(int x){
        if (x != father[x]){
            father[x] = findSet(father[x]);
        }
        return father[x];
    }
    void unionSet(int x, int y){
        int fx = findSet(x);
        int fy = findSet(y);
        if (fx != fy){
            father[fx] = fy;
            setsize[fy] += setsize[fx];
        }
    }
    int largestIsland(vector<vector<int>>& grid) {
        int n = grid.size();
        initSet(n * n);
        for (int i = 0;i<n;i++){
            for(int j = 0;j<n;j++){
                if (grid[i][j] == 0){
                    continue;
                }
                else{
                    for (auto dir : dirs){
                        int x = i + dir[0], y = j + dir[1];
                        if (x < 0 || x >= n || y < 0 || y >= n || grid[x][y] != 1){
                            continue;
                        }
                        unionSet(i * n + j, x * n + y);
                    }
                }
            }
        }
        int ans = 0;
        for (int i = 0;i<n;i++){
            for (int j = 0;j<n;j++){
                if (grid[i][j] == 0){
                    int res = 1;
                    //防止重复加入
                    unordered_set<int> ust;
                    for (auto dir : dirs){
                        int x = i + dir[0], y = j + dir[1];
                        if (x < 0 || x >= n || y < 0 || y >= n || grid[x][y] == 0) continue;
                        int fn = findSet(x * n + y);
                        if (!ust.count(fn)){
                            res += setsize[fn];
                            ust.insert(fn);
                        }
                    }
                    ans = max(ans, res);
                }
                //防止全1矩阵
                else{
                    ans = max(ans, setsize[findSet(i * n + j)]);
                }
            }
        }
        return ans;
    }
};
cpp
//洪水填充做法
class Solution {
public:
    int dirs[4][2] = {{-1, 0}, {0, -1}, {0, 1}, {1, 0}};
    void dfs(vector<vector<int>> & g, int i, int j, int id){
        int n = g.size();
        if(i < 0 || i == n || j < 0 || j == n || g[i][j] != 1){
            return;
        }
        g[i][j] = id;
        for (auto dir : dirs){
            dfs(g, i + dir[0], j + dir[1], id);
        }
    }
    int largestIsland(vector<vector<int>>& grid) {
        int n = grid.size();
        int id = 2;
        for (int i = 0;i<n;i++){
            for (int j = 0;j<n;j++){
                if(grid[i][j] == 1){
                    dfs(grid, i, j, id);
                    id++;
                }
            }
        }
        vector<int> sz(id, 0);//id是变量
        int ans = 0;
        for (int i = 0;i<n;i++){
            for (int j = 0;j<n;j++){
                if (grid[i][j] > 1){
                    ans = max(ans, ++sz[grid[i][j]]);
                }
            }
        }
        unordered_set<int> ust;
        for(int i = 0;i<n;i++){
            for (int j = 0;j<n;j++){
                ust.clear();
                if (grid[i][j] == 0){
                    int new_area = 1;
                    for (auto & [dx, dy] : dirs){
                        int x = i + dx, y = j + dy;
                        if (x < 0 || x >= n || y < 0 || y >= n || grid[x][y] == 0){
                            continue;
                        }
                        if (!ust.count(grid[x][y])){
                            new_area += sz[grid[x][y]];
                            ust.insert(grid[x][y]);
                        }
                    }
                    ans = max(ans, new_area);
                }
            }
        }
        return ans;
    }
};
```

## leetcode No.803 打砖块

[原题](https://leetcode.cn/problems/bricks-falling-when-hit/description/)

有一个 `m x n` 的二元网格 `grid` ，其中 `1` 表示砖块，`0` 表示空白。砖块 **稳定**（不会掉落）的前提是：

- 一块砖直接连接到网格的顶部，或者
- 至少有一块相邻（4 个方向之一）砖块 **稳定** 不会掉落时

给你一个数组 `hits` ，这是需要依次消除砖块的位置。每当消除 `hits[i] = (rowi, coli)` 位置上的砖块时，对应位置的砖块（若存在）会消失，然后其他的砖块可能因为这一消除操作而 **掉落** 。一旦砖块掉落，它会 **立即** 从网格 `grid` 中消失（即，它不会落在其他稳定的砖块上）。

返回一个数组 `result` ，其中 `result[i]` 表示第 `i` 次消除操作对应掉落的砖块数目。

**注意**，消除可能指向是没有砖块的空白位置，如果发生这种情况，则没有砖块掉落。



**示例 1：**

```
输入：grid = [[1,0,0,0],[1,1,1,0]], hits = [[1,0]]
输出：[2]
解释：网格开始为：
[[1,0,0,0]，
 [1,1,1,0]]
消除 (1,0) 处加粗的砖块，得到网格：
[[1,0,0,0]
 [0,1,1,0]]
两个加粗的砖不再稳定，因为它们不再与顶部相连，也不再与另一个稳定的砖相邻，因此它们将掉落。得到网格：
[[1,0,0,0],
 [0,0,0,0]]
因此，结果为 [2] 。
```

**示例 2：**

```
输入：grid = [[1,0,0,0],[1,1,0,0]], hits = [[1,1],[1,0]]
输出：[0,0]
解释：网格开始为：
[[1,0,0,0],
 [1,1,0,0]]
消除 (1,1) 处加粗的砖块，得到网格：
[[1,0,0,0],
 [1,0,0,0]]
剩下的砖都很稳定，所以不会掉落。网格保持不变：
[[1,0,0,0],
 [1,0,0,0]]
接下来消除 (1,0) 处加粗的砖块，得到网格：
[[1,0,0,0],
 [0,0,0,0]]
剩下的砖块仍然是稳定的，所以不会有砖块掉落。
因此，结果为 [0,0] 。
```



**提示：**

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 200`
- `grid[i][j]` 为 `0` 或 `1`
- `1 <= hits.length <= 4 * 104`
- `hits[i].length == 2`
- `0 <= xi <= m - 1`
- `0 <= yi <= n - 1`
- 所有 `(xi, yi)` 互不相同

```cpp
class Solution {
public:
    int n, m;
    vector<vector<int>> grid;
    //从i行j列这个格子出发，遇到1就感染成2，统计新增了几个2
    int dfs(int i, int j){
        if (i < 0 || i == n || j < 0|| j == m || grid[i][j] != 1){
            return 0;
        }
        grid[i][j] = 2;
        return 1 + dfs(i + 1, j) + dfs(i, j + 1) + dfs(i - 1, j) + dfs(i, j - 1);
    }
    bool worth(int i, int j){
        return grid[i][j] == 1 && (i == 0 || (i > 0 && grid[i-1][j] == 2) || (i < n-1 && grid[i+1][j] == 2) || (j > 0 && grid[i][j-1] == 2) || (j < m-1 && grid[i][j+1] == 2));
    }
    vector<int> hitBricks(vector<vector<int>>& g, vector<vector<int>>& hits) {
        grid = g;
        n = grid.size();
        m = grid[0].size();
        vector<int> ans(hits.size(), 0);
        if(n == 1){
            return ans;
        }
        for (auto hit : hits){
            grid[hit[0]][hit[1]]--;
        }
        //天花板洪水填充
        for (int i = 0;i<m;i++){
            dfs(0, i);
        }
        //时光倒流
        for (int i = hits.size() - 1, row, col; i >= 0;i--){
            row = hits[i][0];
            col = hits[i][1];
            grid[row][col]++;
            if (worth(row, col)){
                ans[i] = dfs(row, col) - 1;
            }
        }
        return ans;
    }
};
```
