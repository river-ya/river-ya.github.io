这份索引整理自 `ACwing/zuoshen` 里的随堂笔记。每个专题都能直接读到原来的推导、练习和代码。刚做完《跳石头》可以先看二分答案；想追《新汉诺塔》的递归过程，可以从 DFS 里的系统栈和子问题入手。

## 从二分到排序

| 笔记 | 阅读线索 |
| --- | --- |
| [二分搜索](/knowledge/algorithms/binary-search/) · [二分答案](/knowledge/algorithms/binary-answer/) | 前一篇处理有序数组左右边界，用对数器检查实现；后一篇把“答案是多少”改成可行性判断，练习里有吃香蕉、画匠分割和第 K 小的数对距离。 |
| [位运算](/knowledge/algorithms/bits-basics/) | 从补码和异或开始，利用最低位的 1，把两种出现奇数次的数字分到不同组。 |
| [归并排序](/knowledge/algorithms/merge-sort/) · [堆排序](/knowledge/algorithms/heap/) | 对照归并时的辅助数组与大根堆的原地交换。堆笔记标出了向上调整时传“下标”和传“元素值”的区别。 |

## 线性结构与区间

| 笔记 | 阅读线索 |
| --- | --- |
| [栈与队列](/knowledge/algorithms/stack-queue/) · [链表](/knowledge/algorithms/linked-list/) | 从循环队列的下标管理、双端队列，到链表反转时保存尚未处理的后继节点。 |
| [前缀和](/knowledge/algorithms/prefix-sum/) · [差分](/knowledge/algorithms/difference/) | 一个侧重查询区间和，另一个侧重批量修改区间；例题包括和为 K 的子数组、航班预订和等差数列修改。 |
| [滑动窗口](/knowledge/algorithms/sliding-window/) | 比较最短达标子数组、无重复字符子串和最小覆盖子串中，左边界分别在什么时候能前移。 |
| [单调栈](/knowledge/algorithms/monotonic-stack/) | 从每日温度、柱状图最大矩形，到按贡献统计子数组最小值。相等元素的处理决定一个区间会不会被重复计数。 |

## 递归、树与字符串

| 笔记 | 阅读线索 |
| --- | --- |
| [递归与 DFS](/knowledge/algorithms/recursion/) | 收录子序列、去重全排列、嵌套解析和 N 皇后。文末附《外星密码》和《赦免战俘》的原练习代码。 |
| [二叉树遍历](/knowledge/algorithms/binary-tree/) | 对照递归和显式栈的前、中、后序遍历，再看按层和锯齿形遍历。 |
| [前缀树](/knowledge/algorithms/trie/) | 比较动态节点与静态数组建树，练习包括数对最大异或值和在棋盘上查找多个单词。 |
| [KMP](/knowledge/algorithms/kmp/) | 从一张手推表读懂 `next` 数组：已匹配前缀能保留多长，决定了失配后模式串退到哪里。 |

## 图与动态规划

| 笔记 | 阅读线索 |
| --- | --- |
| [并查集](/knowledge/algorithms/union-find/) · [洪水填充](/knowledge/algorithms/flood-fill/) | 从路径压缩、小集合挂大集合，到网格中的岛屿标记和区域连通性。 |
| [建图与拓扑排序](/knowledge/algorithms/topological-sort/) · [Floyd 最短路](/knowledge/algorithms/shortest-path/) | 一边按入度安排有先后依赖的任务，一边逐个开放中转点来更新距离矩阵。 |
| [最大公约数与同余](/knowledge/algorithms/gcd/) | 欧几里得算法、公倍数和取模，是原动态规划笔记开篇用到的数学工具。 |
| [从递归到动态规划](/knowledge/algorithms/dp-basics/) · [子数组与子矩阵](/knowledge/algorithms/max-subarray/) | 跟着一维、二维、三维状态看哪些递归参数要进表，再看如何按上下边界压缩矩阵。 |

## 三份 CSP 练习源码

- [化学方程式配平检查 · csp201912C.cpp](/assets/notes/zuoshen/csp201912C.cpp)。按等号和加号切分，用递归处理括号和倍数，最后比较左右两侧的元素计数。
- [咖啡分配 · csp41_T2.cpp](/assets/notes/zuoshen/csp41_T2.cpp)。整组分配的任务用倒序背包，可拆分的任务按每杯咖啡带来的耗时缩减排序，再枚举两类任务之间的预算分配。
- [接口内存模拟 · csp41_T3.cpp](/assets/notes/zuoshen/csp41_T3.cpp)。用有序集合记录空闲地址段，模拟申请、发送和释放合并。原实现的空闲段使用 `long long`，接口端点却使用 `int`；测试大于 32 位范围的地址时要留意这个边界。

课程对应左程云的《算法通关》系列。这里收录的是学习笔记和练习，课程材料可以到作者仓库查阅。[课程仓库](https://github.com/algorithmzuo/algorithm-journey)
