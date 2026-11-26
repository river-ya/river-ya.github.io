# kmp算法原理

1. 理解next数组

**不含当前，前后缀最大匹配长度（不含整体）**

a	a	b	a	a	b	s	a	a	b	a	a	a	|终止位置

0	1	2	3	4	5	6	7	8	9	10     11     12	|13

-1	0	1	0	1	2	3	0	1	2	3	4	5	|2

2. 假设已经有了next数组，匹配过程是如何加速的，加速过程的理解

![课堂推演图 1](/assets/notes/zuoshen/kmp-01.jpg)

3.next数组如何快速生成

```cpp
vector<int> next_array(string s, int m){
    if(m == 1){
        return {-1};
    }
    vector<int> next(m, 0);
    next[0] = -1;
    next[1] = 0;
    // i表示当前要求next值的位置
    // cn表示当前要和前一个字符比对的下标
    int i = 2, cn = 0;
    while (i < m){
        if (s[i - 1] == s[cn]){
            next[i++] = ++cn;
        }
        else if(cn > 0){
            cn = next[cn];
        }
        else{
            next[i++] = 0;
        }
    }
    return next;
}
int kmp(string s1, string s2){
    // s1中当前比对的位置是x
    // s2中当前比对的位置是y
    int n = s1.size(), m = s2.size();
    int x = 0, y = 0;
    //O(m)
    vector<int> next = next_array(s2, m);
    //两个比对位置都不越界
    //O(n)
    while (x < n && y < m){
        if (s1[x] == s2[y]){
            x++;
            y++;
        }
        else if(y == 0){
            x++;
        }
        else{
            y = next[y];
        }
    }
    return y == m ? x - y : -1; //如果y越界说明找到了，返回x - y即字符串开头的位置，否则返回-1
}
```
