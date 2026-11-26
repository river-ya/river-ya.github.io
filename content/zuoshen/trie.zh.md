# 前缀树/字典树

## 1.基础知识

每个样本都从头节点开始，根据前缀字符或前缀数字建出来的一颗大树就是前缀树（信息一般都放在**路**上）**没有路就新建节点，已经有路了就复用节点**

* 前缀树使用场景：需要根据前缀信息来查询的场景
* 前缀树的优点：根据前缀信息选择树上的分支，可以节省大量的时间
* 前缀树的缺点：比较浪费空间，和**总字符的数量、字符的种类**有关
* 前缀树的定制：pass，end等信息

## 2.动态实现Trie类

1. Trie(),初始化前缀树对象
2. void insert(string word) 将字符串word插入前缀树中
3. int search(string word) 返回前缀树中字符串word的实例个数
4. int prefixNumber(string prefix) 返回前缀树中以prefix为前缀的字符串个数
5. void delete(string word) 删除前应该先判断该字符串是否存在，再从前缀树中移除字符串word（一次）

```cpp
class Trie{
    struct Trienode{
        int pass;
        int end;
        Trienode * nexts[26];
        Trienode(){
            pass = end = 0;
            for(int i = 0;i<26;i++){
                nexts[i] = nullptr;
            }
        }
    };
    private:
        Trienode* root;
        // 递归释放所有节点内存
        void destroy(Trienode* node) {
            if (node == nullptr) return;
            // 先释放所有子节点
            for (int i = 0; i < 26; i++) {
                destroy(node->nexts[i]);
            }
            // 再释放自己
            delete node;
        }
    public:
        Trie(){
            root = new Trienode();
        }
        // 析构函数：自动释放内存
        ~Trie() {
            destroy(root);
        }
        void insert(string word){
            Trienode* node = root;
            node->pass++;
            for (int i = 0, path;i<word.size();i++){
                path = word[i] - 'a';//假设word由小写字母组成
                if (node->nexts[path] == nullptr){
                    node->nexts[path] = new Trienode();
                }
                node = node->nexts[path];
                node->pass++;
            }
            node->end++;
        }
        //查询word出现了几次
        int search(string word){
            Trienode* node = root;
            for (int i = 0,path;i<word.size();i++){
                path = word[i] - 'a';
                if (node->nexts[path] == nullptr){
                    return 0;
                }
                node = node->nexts[path];
            }
            return node->end;
        }
        //查询有多少单词以prefix做前缀
        int prefixNumber(string prefix){
            Trienode * node = root;
            for (int i = 0, path;i<prefix.size();i++){
                path = prefix[i] - 'a';
                if (node->nexts[path] == nullptr) return 0;
                node = node->nexts[path];
            }
            return node->pass;
        }
        //如果之前word插入过前缀树，那么此时删掉一次
        //如果之前word没有插入过前缀树，那么不做处理
        void del(string word){
            if(search(word) > 0){
                Trienode * node = root;
                node->pass--;
                for (int i = 0, path;i<word.size();i++){
                    path = word[i] - 'a';
                    if (--node->nexts[path]->pass == 0){
                        delete node->nexts[path];
                        node->nexts[path] = nullptr;
                        return;
                    }
                    node = node->nexts[path];
                }
                node->end--;
            }
        }
};
```

我们发现不一定只有小写字母，我们的nexts数组难道要开65535这么大吗，显然不合理
所以我们可以采用hashmap，实现方式这里不做展示（因为正常打算法竞赛也不会用动态Trie类）

## 3.静态数组实现Trie

更推荐如下静态数组的方式实现Trie

```cpp
class Trie{
private:
    static const int MAXN = 150001;
    int tree[MAXN][26];
    int end[MAXN];
    int pass[MAXN];
    int cnt;
public:
    Trie(){
        cnt = 1;
        for (int i = 0;i<MAXN;i++){
            pass[i] = end[i] = 0;
            for (int j = 0;j<26;j++){
                tree[i][j] = 0;
            }
        }
    }
    void insert(string word){
        int cur = 1;
        pass[cur]++;
        for (int i = 0, path; i < word.size();i++){
            path = word[i] - 'a';
            if (tree[cur][path] == 0){
                tree[cur][path] = ++cnt;
            }
            cur = tree[cur][path];
            pass[cur]++;
        }
        end[cur]++;
    }
    int search(string word){
        int cur = 1;
        for (int i = 0,path;i<word.size();i++){
            path = word[i] - 'a';
            if (tree[cur][path] == 0) return 0;
            cur = tree[cur][path];
        }
        return end[cur];
    }
    int prefixNumber(string prefix){
        int cur = 1;
        for (int i = 0,path;i<prefix.size();i++){
            path = prefix[i] - 'a';
            if (tree[cur][path] == 0) return 0;
            cur = tree[cur][path];
        }
        return pass[cur];
    }
    void del(string word){
        if (search(word) > 0){
            int cur = 1;
            pass[cur]--;
            for (int i = 0, path;i<word.size();i++){
                path = word[i] - 'a';
                if (--pass[tree[cur][path]] == 0){
                    tree[cur][path] = 0;
                    return;
                }
                cur = tree[cur][path];
            }
            end[cur]--;
        }
    }
};
```

同样，如果路很多呢？
别急，之后有具体题目（

## 4.前缀树的相关题目

### T1 接头密匙 newcode

[原题](https://www.nowcoder.com/practice/c552d3b4dfda49ccb883a6371d9a6932)

描述
牛牛和他的朋友们约定了一套接头密匙系统，用于确认彼此身份。密匙由一组数字序列表示，两个密匙被认为是一致的，如果满足以下条件：

密匙 b 的长度不超过密匙 a 的长度。
对于任意 0 <= i < length(b)，有 b[i+1] - b[i] == a[i+1] - a[i]。
现在给定了m个密匙 b 的数组，以及n个密匙 a 的数组。请你返回一个长度为 m 的结果数组 ans，表示每个密匙b都有多少一致的密匙a。
示例1
输入：
[[1, 2, 3, 4, 5], [2, 4, 6, 8], [1, 4, 7, 10]],[[3, 4, 5, 6, 7, 8], [2, 4, 6, 8], [1, 3, 5, 7, 9]]

返回值：[1,2,0]

说明：
与 b[0] 数组一致的 a 数组有一个：a[0]。
与 b[1] 数组一致的 a 数组有两个：a[1]和a[2]。
与 b[2] 数组一致的 a 数组没有。
示例2
输入：
[[1, 2, 3], [4, 5, 6, 7, 8], [2, 4, 6, 8]],[[1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7, 8], [1, 4, 7, 10]]

返回值：[2,2,0]

说明：

备注：
数组 a 和数组 b 中的元素个数均不超过 10^5。
1 <= m, n <= 1000

* 这个问题就很可能出现很大的数字，比如997这种差值，那么我们可以把它拆分成9->9->7->#,"#"为终止符来区分不同差值

```cpp
class Trie{
private:
    static const int MAXN = 150001;
    int tree[MAXN][12];
    int end[MAXN];
    int pass[MAXN];
    int cnt;
public:
    Trie(){
        cnt = 1;
        for (int i = 0;i<MAXN;i++){
            pass[i] = end[i] = 0;
            for (int j = 0;j<12;j++){
                tree[i][j] = 0;
            }
        }
    }
    //核心改动
    int get_path(char c){
        if (c == '#'){
            return 10;
        }
        if (c == '-'){
            return 11;
        }
        return c - '0';
    }
    void insert(string word){
        int cur = 1;
        pass[cur]++;
        for (int i = 0, path; i < word.size();i++){
            path = get_path(word[i]);
            if (tree[cur][path] == 0){
                tree[cur][path] = ++cnt;
            }
            cur = tree[cur][path];
            pass[cur]++;
        }
        end[cur]++;
    }
    int prefixNumber(string prefix){
        int cur = 1;
        for (int i = 0,path;i<prefix.size();i++){
            path = get_path(prefix[i]);
            if (tree[cur][path] == 0) return 0;
            cur = tree[cur][path];
        }
        return pass[cur];
    }
};
//但是牛客不让用c风格数组，我将其改为array类型，完整代码如下
class Solution {
  public:
    class Trie {
      private:
        static const int MAXN = 150001;
        // 每个节点有 12 个孩子：0-9, '#', '-'
        array<array<int, 12>, MAXN> tree{};
        array<int, MAXN> end{};
        array<int, MAXN> pass{};
        int cnt;
        int get_path(char c) {
            if (c == '#') return 10;
            if (c == '-') return 11;
            return c - '0';
        }

      public:
        Trie() : cnt(1) {
            for (auto& row : tree) {
                row.fill(0);
            }
            pass.fill(0);
            end.fill(0);
        }

        void insert(const string& word) {
            int cur = 1;
            pass[cur]++;
            for (char c : word) {
                int path = get_path(c);
                if (tree[cur][path] == 0) {
                    tree[cur][path] = ++cnt;
                }
                cur = tree[cur][path];
                pass[cur]++;
            }
            end[cur]++;
        }

        int prefixNumber(const string& prefix) {
            int cur = 1;
            for (char c : prefix) {
                int path = get_path(c);
                if (tree[cur][path] == 0) return 0;
                cur = tree[cur][path];
            }
            return pass[cur];
        }

        int search(const string& word) {
            int cur = 1;
            for (char c : word) {
                int path = get_path(c);
                if (tree[cur][path] == 0) return 0;
                cur = tree[cur][path];
            }
            return end[cur];
        }

        void del(const string& word) {
            if (search(word) == 0) return;
            int cur = 1;
            pass[cur]--;
            for (char c : word) {
                int path = get_path(c);
                int nxt = tree[cur][path];
                if (--pass[nxt] == 0) {
                    tree[cur][path] = 0;
                    return;
                }
                cur = nxt;
            }
            end[cur]--;
        }
    };
    vector<int> countConsistentKeys(vector<vector<int> >& b,
                                    vector<vector<int> >& a) {
        int m = b.size();
        int n = a.size();
        vector<int> ans;
        Trie trie;
        for (int i = 0;i<n;i++){
            int size = a[i].size();
            string str = "";
            for (int j = 1;j<size;j++){
                str += to_string(a[i][j] - a[i][j-1]) + '#';
            }
            trie.insert(str);
        }
        for(int i = 0;i<m;i++){
            int size = b[i].size();
            string str = "";
            for(int j = 1;j<size;j++){
                str += to_string(b[i][j] - b[i][j-1]) + '#';
            }
            ans.push_back(trie.prefixNumber(str));
        }
        return ans;
    }
};

```

### T2 数组中两个数的最大异或值 leetcode LCR 067

[原题](https://leetcode.cn/problems/ms70jA/)

给定一个长度为 n 的数组，请你返回任选两个数的最大异或值。
数据范围：1 <= n <= 10^4, 数组中的满足 0 <= val <= 10^9

```cpp
//int 32位，根据数据范围则保证第一位一定是0，那么我们可以找max来减少前缀树深度，用left来标记位置，避免了每次对前导零的异或操作
class Solution {
public:
    class Trie {
    private:
        static const int MAXN = 3000001;
        int tree[MAXN][2];
        int cnt;
        int left;//数字需要从第几位开始考虑
    public:
        Trie() {
            cnt = 1;
            for (int i = 0; i < MAXN; i++) {
                for (int j = 0; j < 2; j++) {
                    tree[i][j] = 0;
                }
            }
        }
        int leadingzero(int num){
            int cnt = 0;
            for (int i = 31; i >= 0; --i) {
                if (num & (1 << i)) break;
                ++cnt;
            }
            return cnt;
        }
        void build(vector<int> & nums){
            cnt = 1;
            int max_ = INT_MIN;
            for(int & num : nums){
                max_ = max(max_,num);
            }
            //计算数组最大值的二进制状态，有多少前缀零
            //可以忽略这些前缀的0，从left位开始
            left = 31 - leadingzero(max_);
            for(int & num : nums){
                insert(num);
            }
        }
        void insert(int num) {
            int cur = 1;
            for (int i = left, path; i >= 0; i--) {
                path = (num >> i) & 1;
                if (tree[cur][path] == 0) {
                    tree[cur][path] = ++cnt;
                }
                cur = tree[cur][path];
            }
        }
        int maxXor(int num) {
            int ans = 0;//最终异或的结果(尽量大)
            int cur = 1;//目前的节点编号
            for (int i = left, status, want; i >= 0; i--) {
                status = (num >> i) & 1;//num第i位的状态
                want = status ^ 1;//希望遇到的状态
                if (tree[cur][want] == 0)//询问前缀树，能不能达成
                    //达成不了
                    want ^= 1;
                //want变成真正往下走的路
                ans |= (status ^ want) << i;
                cur = tree[cur][want];
            }
            return ans;
        }
    };
    int findMaximumXOR(vector<int>& nums) {
        Trie trie;
        trie.build(nums);
        int ans = 0;
        for (int num : nums){
            ans = max(ans, trie.maxXor(num));
        }
        return ans;
    }
};
```

还有一种哈希表的做法，但比较难想
异或运算的性质：
a ^ b == c -> b == a ^ c && a == b ^ c

```cpp
class Solution {
public:
    int leadingzero(int num){
        int cnt = 0;
        for (int i = 31; i >= 0; --i) {
            if (num & (1 << i)) break;
            ++cnt;
        }
        return cnt;
    }
    int findMaximumXOR(vector<int>& nums) {
        int max_ = INT_MIN;
        for (int num : nums){
            max_ = max(max_,num);
        }
        int ans = 0;
        unordered_set<int> st;
        for (int i = 31 - leadingzero(max_);i>=0;i--){
            //ans 从31位到i+1位已经达到的目标
            //讨论第i位能不能达成1的目标
            int better = ans | (1 << i);
            st.clear();
            for(int num : nums){
                //num: 31………… i这些状态，其他全变成0
                num = (num>>i)<<i;
                st.insert(num);
                //num->       达成better目标
                //if s^s'==better, then s' = s ^ better
                if (st.count(better ^ num)){
                    ans = better;
                    break;
                }
            }
        }
        return ans;
    }
};
//时间复杂度： O(n * log max)
//空间复杂度： O(n * log max)
```

### T3 单词搜索II leetcode No.212

[原题](https://leetcode.cn/problems/word-search-ii/description/?envType=problem-list-v2&envId=trie)

给定一个 `m x n` 二维字符网格 `board` 和一个单词（字符串）列表 `words`， *返回所有二维网格上的单词* 。

单词必须按照字母顺序，通过 **相邻的单元格** 内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母在一个单词中不允许被重复使用。



**示例 1：**

[原题配图](https://assets.leetcode.com/uploads/2020/11/07/search1.jpg)

```
输入：board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
输出：["eat","oath"]
```

**示例 2：**

[原题配图](https://assets.leetcode.com/uploads/2020/11/07/search2.jpg)

```
输入：board = [["a","b"],["c","d"]], words = ["abcb"]
输出：[]
```



**提示：**

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `board[i][j]` 是一个小写英文字母
- `1 <= words.length <= 3 * 104`
- `1 <= words[i].length <= 10`
- `words[i]` 由小写英文字母组成
- `words` 中的所有字符串互不相同

```cpp
//剪枝大魔王
class Solution {
public:
    vector<string> ans;
    static const int MAXN = 8000;
    int tree[MAXN][26];
    int pass[MAXN];
    string end[MAXN];
    int cnt;
    void insert(string word){
        int cur = 1;
        pass[cur]++;
        for (int i = 0, path;i<word.size();i++){
            path = word[i] - 'a';
            if (tree[cur][path] == 0){
                tree[cur][path] = ++cnt;
            }
            cur = tree[cur][path];
            pass[cur]++;
        }
        end[cur] = word;
    }
    void build(vector<string> & words){
        cnt = 1;
        for (int i = 0;i<MAXN;i++){
            end[i] = "";
            pass[i] = 0;
            for (int j = 0;j<26;j++){
                tree[i][j] = 0;
            }
        }
        for (string & word : words){
            insert(word);
        }
    }
    //i, j 此时来到的位置
    //cur: 前缀树的编号
    //关键剪枝：返回收集到了几个字符串
    int dfs(vector<vector<char>>& board, int i, int j, int cur){
        //越界或者走了回头路，直接返回0
        if(i < 0|| j < 0 || i == board.size() || j == board[0].size() || board[i][j] == 0){
            return 0;
        }
        char tmp = board[i][j];
        int path = tmp - 'a';
        int cur = tree[cur][path];
        //本来就没有路或者之前的路已被删除
        if (pass[cur] == 0){//cur=0时pass数组也是0
            return 0;
        }
        //fix：从当前位置出发，一共收集到了几个字符串
        int fix = 0;
        if (end[cur] != ""){
            ans.push_back(end[cur]);
            fix++;
            end[cur] = "";//剪枝,不再收集此单词
        }
        //后续过程不允许再来到i，j位置
        board[i][j] = 0;//省的再开一个二维数组
        fix += dfs(board, i-1, j, cur);
        fix += dfs(board, i, j-1, cur);
        fix += dfs(board, i+1, j, cur);
        fix += dfs(board, i, j+1, cur);
        pass[cur] -= fix;//剪枝,收集过的就不再收集了
        //恢复现场
        board[i][j] = tmp;
        return fix;
    }
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        int m = board.size();
        int n = board[0].size();
        build(words);
        for (int i = 0;i < m;i++){
            for (int j = 0;j<n;j++){
                dfs(board, i, j, 1);
            }
        }
        return ans;
    }
};
```
