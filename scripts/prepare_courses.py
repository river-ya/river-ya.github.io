"""Reproduce the course-to-topic mapping from the committed source snapshot."""
import json,re
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
def bi(a,b):return {'zh-CN':a,'en':b}
categories=[('basics','入门与验证','Foundations'),('structures','基础数据结构','Data structures'),('sorting','分治与排序','Divide & conquer'),('bits','位运算与递归','Bits & recursion'),('arrays','数组与区间','Arrays & intervals'),('monotonic','单调结构与集合','Monotonic structures'),('graphs','图论基础','Graph algorithms'),('dp','动态规划基础','Dynamic programming'),('dp-topics','动态规划专题','DP patterns'),('math','贪心与数学','Greedy & mathematics'),('strings','字符串','Strings'),('ranges','区间数据结构','Range structures'),('trees','树上算法','Tree algorithms'),('advanced','进阶 DP 与数学','Advanced DP & mathematics'),('expert','有序结构与高级专题','Advanced structures'),('strategy','学习策略与工程','Study & engineering')]
spec='''
bits-basics|位运算基础|Bit operations|basics|003|表示整数与按位操作|Represent integers and manipulate bits
elementary-sorting|基础排序|Elementary sorting|basics|004|理解排序过程与循环不变量|Understand sorting and loop invariants
test-harness|对数器|Randomized test harness|basics|005,042|用暴力解验证优化算法|Check optimized algorithms against a brute-force oracle
binary-search|二分搜索|Binary search|basics|006|在有序或单调空间定位边界|Locate boundaries in ordered or monotonic spaces
complexity|复杂度分析|Complexity analysis|basics|007,008|估计时间与空间开销|Estimate time and space costs
io|输入输出|Input & output|basics|019|处理算法题的输入输出协议|Handle input and output formats
linked-list|链表|Linked lists|structures|009-012,034|维护链接与局部结构变化|Maintain links and local structural changes
stack-queue|栈与队列|Stacks & queues|structures|013-015,035|组织后进先出与先进先出操作|Organize LIFO and FIFO operations
deque|双端队列|Deque|structures|016|支持两端插入与删除|Support insertion and removal at both ends
binary-tree|二叉树遍历|Binary tree traversal|structures|017,018,036,037|用递归与显式栈遍历树|Traverse trees recursively or with explicit stacks
recurrence|递归与 Master 公式|Recurrences & Master theorem|sorting|020|分析递归子问题与合并成本|Analyze recursive subproblems and merge costs
merge-sort|归并与分治|Merge sort & divide and conquer|sorting|021,022|分解问题并统计跨区间信息|Divide problems and combine information across ranges
quick-sort|快排与随机选择|Quicksort & quickselect|sorting|023,024|通过随机划分缩小问题规模|Reduce problems through randomized partitioning
heap|堆与优先队列|Heaps & priority queues|sorting|025,027|维护动态极值与优先级|Maintain dynamic extrema and priorities
radix-sort|基数排序|Radix sort|sorting|028,029|利用位或数位结构组织排序|Sort by digits or bit structure
xor|异或技巧|XOR techniques|bits|030,031,033|利用按位运算的代数性质|Use algebraic properties of bitwise operations
bitmap|位图|Bitmap|bits|032|用位集合压缩存在性信息|Compress membership information into bits
recursion|递归枚举|Recursive enumeration|bits|038,039|建立状态与递归返回值|Define states and recursive return values
n-queens|N 皇后|N-queens|bits|040|在约束中枚举并剪枝|Enumerate and prune under constraints
prefix-sum|前缀和|Prefix sums|arrays|046,048|把区间查询变成前缀差|Express range queries as prefix differences
difference|差分与离散化|Difference arrays & compression|arrays|047,048|高效表达区间更新|Represent range updates efficiently
sliding-window|滑动窗口|Sliding window|arrays|049|维护连续区间中的约束|Maintain constraints over contiguous windows
two-pointers|双指针|Two pointers|arrays|050|协调两个位置缩小搜索范围|Coordinate two indices to narrow a search
binary-answer|二分答案|Binary search on the answer|arrays|051|利用判定问题的单调性|Exploit monotonicity of a decision problem
monotonic-stack|单调栈|Monotonic stack|monotonic|052,053|寻找相邻更大或更小元素|Find neighboring greater or smaller elements
monotonic-queue|单调队列|Monotonic queue|monotonic|054,055|维护窗口极值|Maintain extrema in a moving window
union-find|并查集|Disjoint-set union|monotonic|056,057|维护集合合并与连通关系|Maintain set unions and connectivity
flood-fill|洪水填充|Flood fill|monotonic|058|遍历网格连通区域|Traverse connected regions in a grid
topological-sort|建图与拓扑排序|Graph construction & topological sort|graphs|059,060|处理依赖关系与有向无环图|Handle dependencies and directed acyclic graphs
mst|最小生成树|Minimum spanning tree|graphs|061|以最小代价连接所有顶点|Connect all vertices with minimum total cost
bfs|宽度优先遍历|Breadth-first search|graphs|062,063|逐层探索与双向搜索|Explore by layers and search bidirectionally
shortest-path|最短路|Shortest paths|graphs|064,065|根据边权性质选择路径算法|Choose path algorithms according to edge weights
dp-basics|从递归到动态规划|From recursion to DP|dp|066-069|定义状态、转移和边界|Define states, transitions, and base cases
max-subarray|子数组问题|Subarray problems|dp|070,071|维护连续区间的最优状态|Maintain optimal states over contiguous ranges
lis|最长递增子序列|Longest increasing subsequence|dp|072|处理子序列顺序约束|Handle ordering constraints in subsequences
knapsack-dp|背包 DP|Knapsack DP|dp-topics|073-075|在容量约束下分配选择|Choose items under capacity constraints
interval-dp|区间 DP|Interval DP|dp-topics|076,077|通过区间划分或端点组织状态|Organize states by interval splits or endpoints
tree-dp|树形 DP|Tree DP|dp-topics|078,079|汇总子树状态解决全局问题|Combine subtree states to solve a global problem
bitmask-dp|状压 DP|Bitmask DP|dp-topics|080,081|用集合编码有限状态|Encode finite set states with bitmasks
dp-optimization|枚举优化与方案恢复|DP optimization & reconstruction|dp-topics|082,083,086-088|优化转移并恢复决策路径|Optimize transitions and reconstruct decisions
digit-dp|数位 DP|Digit DP|dp-topics|084,085|按数位处理受约束整数计数|Count constrained integers digit by digit
gcd|公约数与同余|GCD & congruence|math|041|分析整除与余数关系|Analyze divisibility and remainders
greedy|贪心|Greedy algorithms|math|089-094|用局部选择与交换论证求解|Use local choices and exchange arguments
game-theory|博弈基础|Game theory|math|095,096|分析必胜与必败状态|Analyze winning and losing states
primes|质数筛|Prime sieves|math|097|筛选素数与分解因子|Sieve primes and factor integers
fast-power|快速幂|Fast exponentiation|math|098|用二进制分解加速重复运算|Accelerate repeated operations through binary decomposition
inverse-inclusion|逆元与容斥|Modular inverses & inclusion-exclusion|math|099|处理模除法与重叠计数|Handle modular division and overlapping counts
trie|前缀树|Trie|strings|044,045|按公共前缀组织字符串|Organize strings by shared prefixes
kmp|KMP|KMP|strings|100,101|复用前缀信息避免重复匹配|Reuse prefix information during pattern matching
aho-corasick|AC 自动机|Aho–Corasick|strings|102|在文本中匹配多个模式|Match multiple patterns in text
manacher|Manacher 与扩展 KMP|Manacher & extended KMP|strings|103,104|复用对称或前缀信息|Reuse symmetry and prefix information
string-hash|字符串哈希|String hashing|strings|105|将子串映射到可比较摘要|Map substrings to comparable fingerprints
fenwick|树状数组|Fenwick tree|ranges|108,109|维护动态前缀聚合|Maintain dynamic prefix aggregates
segment-tree|线段树|Segment tree|ranges|110-116|分层维护区间信息与更新|Maintain range aggregates and updates hierarchically
sparse-table|倍增与 ST 表|Binary lifting & sparse tables|ranges|117|预处理静态区间与跳转查询|Preprocess static range and jump queries
lca|最近公共祖先|Lowest common ancestor|trees|118,119|寻找树上路径的公共结构|Find shared structure in tree paths
tree-centroid|重心与直径|Centroids & diameters|trees|120,121|分析树的结构中心与最长路径|Analyze structural centers and longest paths
tree-difference|树上差分与换根|Tree differences & rerooting|trees|122,123|汇总路径更新或切换根节点|Aggregate path updates or change the root
morris|Morris 遍历|Morris traversal|trees|124|利用临时线索完成树遍历|Traverse a tree using temporary threads
profile-dp|轮廓线与进阶 DP|Profile & advanced DP|advanced|125-132|压缩边界状态并优化转移|Compress frontier states and optimize transitions
gaussian-elimination|高斯消元与线性基|Elimination & linear bases|advanced|133-137|求解方程组与维护独立向量|Solve equation systems and maintain independent vectors
fractional|分数规划|Fractional programming|advanced|138|优化比值目标|Optimize ratio objectives
extended-gcd|扩展欧几里得与 CRT|Extended GCD & CRT|advanced|139-141|处理不定方程与同余方程组|Solve Diophantine equations and congruence systems
difference-constraints|差分约束与同余最短路|Difference constraints|advanced|142,143|用路径约束表达数学关系|Express mathematical relations through path constraints
combinatorics|组合计数|Combinatorics|advanced|144-147|运用组合恒等式与计数映射|Use combinatorial identities and counting maps
balanced-trees|平衡树与有序结构|Balanced search trees|expert|148-153|维护动态有序集合|Maintain dynamic ordered sets
meldable-heap|左偏树与 k 短路|Meldable heaps|expert|154,155|支持高效合并的堆结构|Use heaps that support efficient merging
weighted-dsu|带权并查集|Weighted DSU|expert|156|维护集合内的相对关系|Maintain relative relations within sets
persistent|可持久化结构|Persistent structures|expert|157-160,165|查询历史版本并组织多层索引|Query historical versions and organize layered indexes
heavy-light|树链剖分与合并|Heavy-light decomposition|expert|161-164|把树上问题分解为可维护区间|Reduce tree problems to maintainable ranges
offline-divide|离线分治|Offline divide and conquer|expert|166-171|按时间、答案或维度分解问题|Divide problems by time, answer, or dimension
sqrt-decomposition|分块|Square-root decomposition|expert|172-175|平衡块内与块间处理成本|Balance processing within and between blocks
mo|莫队|Mo’s algorithm|expert|176-179|重排离线询问复用区间状态|Reorder offline queries to reuse range state
tree-divide|虚树与点边分治|Virtual trees & centroid decomposition|expert|180-187|压缩关键节点或分解树结构|Compress key vertices or decompose tree structure
connectivity|连通性与欧拉路径|Connectivity & Euler paths|expert|188-194|分析有向与无向图的连通结构|Analyze connectivity in directed and undirected graphs
graph-optimization|优化建图与 2-SAT|Graph optimization & 2-SAT|expert|195-198|压缩依赖关系并求解逻辑约束|Compress dependencies and solve logical constraints
special-graphs|基环树与仙人掌|Special graph structures|expert|199,200|利用图中的特殊环结构|Exploit special cycle structures in graphs
link-cut-tree|动态树 LCT|Link-cut trees|expert|201-204|维护动态森林与路径信息|Maintain dynamic forests and path information
kd-tree|K-D 树|K-D trees|expert|205,206|组织多维空间查询|Organize multidimensional spatial queries
johnson|Johnson 与传递闭包|Johnson & transitive closure|expert|207|处理全源路径与可达关系|Compute all-pairs paths and reachability
study-strategy|学习策略|Study strategies|strategy|001,002,043|组织学习方法与解题策略|Organize study and problem-solving strategies
hash-engineering|哈希与工程专题|Hashing & engineering|strategy|026,106,107|联系算法结构与工程应用|Connect algorithmic structures with engineering
'''
def nums(s):
 out=[]
 for part in s.split(','):
  a,*b=part.split('-');out.extend(range(int(a),int(b[0])+1) if b else [int(a)])
 return [f'{n:03}' for n in out]
topics=[]
for line in spec.strip().splitlines():
 id,zh,en,cat,lessons,desc,desce=line.split('|')
 topics.append(dict(id=id,slug=id,title=bi(zh,en),summary=bi(desc,desce),categoryId=cat,lessonIds=nums(lessons),prerequisiteIds=[],contentStatus='planned',mainContentFiles={},relatedArticleSlugs=[],aliases=[zh,en]))
for t in topics:
 if t['id'] in ['binary-answer','monotonic-stack','knapsack-dp']:t['prerequisiteIds']={'binary-answer':['binary-search'],'monotonic-stack':['stack-queue'],'knapsack-dp':['dp-basics']}[t['id']]
source=json.loads((ROOT/'data/course-source.json').read_text());lessons=[]
for f in source['files']:
 m=re.search(r'算法讲解(\d+)【([^】]+)】(.*)\.(pptx|pdf)$',f['path'])
 if not m:continue
 number,stage,title,_=m.groups()
 lessons.append(dict(id=number,series='algorithm-journey',lessonNumber=number,originalTitle=title.strip(),originalStage=stage,sourceUrl='https://github.com/algorithmzuo/algorithm-journey/blob/'+source['sha']+'/'+quote(f['path']),sourceRef=source['sha'],checkedAt=source['checkedAt'],algorithmIds=[t['id'] for t in topics if number in t['lessonIds']]))
for name,data in [('algorithms',topics),('lessons',lessons),('categories',[dict(id=id,title=bi(zh,en)) for id,zh,en in categories])]:
 (ROOT/'data'/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'{len(lessons)} verified course entries; {len(topics)} topics')
