# 队列和栈
## 1.手搓队列和栈
### 1.1 使用动态数组来实现
```cpp
class Queue{
private:
    int * queue;
    int l;
    int r;
    int capacity;//最大容量
public:
    Queue(int n){
        capacity = n;
        queue = new int[n]; //使用 new[] 动态分配一个包含 n 个整数的数组
        l = 0;
        r = 0;
    }
    //析构函数用来释放内存
    ~Queue(){
        delete[] queue;//使用 delete[] 释放这个数组
    }
    //判空
    bool is_empty(){
        return l == r;
    }
    //入队（这里采用java的命名方法）
    void offer(int num){
        if (r - l == capacity){
            cout << "队列已满，无法添加新元素！" << endl;
            return;
        }
        queue[r++] = num;
    }
    //出队
    int poll(){
        return queue[l++];
    }
    //找队首
    int head(){
        return queue[l];
    }
    //找队尾
    int tail(){
        return queue[r-1];
    }
    int size(){
        return r - l;
    }
};
class Stack{
private:
    int * stack;
    int size;
public:
    Stack(int n){
        stack = new int[n];
        size = 0;
    }
    bool is_empty(){
        return size == 0;
    }
    void push(int num){
        stack[size++] = num;
    }
    int pop(){
        return stack[--size];
    }
    int peek(){
        return stack[size-1];
    }
    int size(){
        return size;
    }
};
```
### 1.2 使用循环数组实现队列，空间利用率高
[设计循环队列 leetcode No.622](https://leetcode.cn/problems/design-circular-queue/description/)
```cpp
class Queue{
private:
    int * queue;
    int l;
    int r;
    int capacity;
    int size;
public:
    Queue(int n){
        capacity = n;
        queue = new int[n]; //使用 new[] 动态分配一个包含 n 个整数的数组
        size = l = r = 0;
    }
    //析构函数用来释放内存
    ~Queue(){
        delete[] queue;//使用 delete[] 释放这个数组
    }
    //判空
    bool is_empty(){
        return size == 0;
    }
    bool is_full(){
        return size == capacity;
    }
    //入队（这里采用java的命名方法）
    void offer(int num){
        if (is_full()){
            cout << "队列已满，无法添加新元素！" << endl;
            return;
        }
        queue[r] = num;
        //r++,结束了，跳回0
        r = (r+1) % capacity;
        size++;
    }
    //出队
    int poll(){
        int tmp = queue[l];
        l = (l+1) % capacity;
        size--;
        return tmp;
    }
    //找队首
    int head(){
        return queue[l];
    }
    //找队尾
    int tail(){
        int last = r == 0 ? (capacity - 1) : (r-1);
        return queue[last];
    }
    int get_size(){
        return size;
    }
};
```
## 2.队列和栈的相互实现
## 3.双端队列
用数组实现双端队列
```cpp
class Deque{
private:
    int * deque;
    int l;
    int r;
    int size;
    int capacity;
public:
    Deque(int n){
        capacity = n;
        size = l = r = 0;
        deque = new int[n];
    }
    bool is_empty(){
        return size == 0;
    }
    bool is_full(){
        return size == capacity;
    }
    void push_front(int num){
        if(is_empty()){
            l = r = 0;
            deque[0] = num;
        }
        else{
            l = l == 0 ? (capacity - 1) : (l-1);
            deque[l] = num;
        }
        size++;
    }
    void push_back(int num){
        if(is_empty()){
            l = r = 0;
            deque[0] = num;
        }
        else{
            r = r == capacity - 1 ? (0) : (r+1);
            deque[r] = num;
        }
        size++;
    }
    int pop_front(){
        if (l == capacity - 1){
            int tmp = deque[l];
            l = 0;
            return tmp;
        }
        else{
            return deque[l++];
        }
        size--;
    }
    int pop_back(){
        if (r == 0){
            int tmp = deque[r];
            r = capacity - 1;
            return tmp;
        }
        else{
            return deque[r--];
        }
        size--;
    }
};
```

## 4.判断出栈元素序列的合理性

**对于任何一个出栈序列，如果其中存在三个元素 pi,pj,pk（它们在出栈序列中的顺序是 pi 在前，pj 在中，pk 在后），并且在原本的入栈序列中，这三个元素的入栈顺序是 pk 最早，pi 其次，pj 最晚，那么这个出栈序列就是不合法的。**

简单来说，**在出栈序列中，任意一个元素后面的所有比它先入栈的元素，必须是降序排列的（即按照它们入栈顺序的逆序排列）。**

## 5.逆波兰表达式

### 5.1中缀表达式转化为后缀表达式

将中缀表达式（我们平时使用的正常数学算式）转换为后缀表达式（逆波兰表达式）的核心原则是：**按照运算符的优先级，将运算符移到它所作用的两个操作数的后面。**

我们可以按照运算的先后顺序一步步来转换表达式 `a * (b + c) - d`：

1. **第一步：处理括号里的加法 `(b + c)`**
   - 运算顺序最高的是括号内的部分。
   - 将 `b + c` 转换为后缀形式：把操作符 `+` 移到操作数 `b` 和 `c` 后面，得到 **`b c +`**。
   - 现在原表达式可以看作：`a * (b c +) - d`。
2. **第二步：处理乘法 `*`**
   - 接下来优先级较高的是乘法。它连接的是 `a` 和刚才的结果 `(b c +)`。
   - 将乘号 `*` 移到这两个部分之后，得到：**`a (b c +) *`**，去掉括号就是 **`a b c + *`**。
   - 现在原表达式可以看作：`(a b c + *) - d`。
3. **第三步：处理减法 `-`**
   - 最后处理减法。它连接的是前面的结果 `(a b c + *)` 和 `d`。
   - 将减号 `-` 移到这两个部分之后，得到：**`(a b c + *) d -`**。
   - 去掉多余的括号，最终的后缀表达式为：**`a b c + * d -`**。

后缀表达式（也叫逆波兰表达式）的运算非常简单且高效，计算机非常喜欢它，因为它**不需要考虑优先级，也不需要括号**，只需要从左到右扫描一遍就可以得出结果。

它的运算核心是借助**“栈”（Stack）**这种数据结构。具体运算规则如下：

运算规则（从左到右扫描表达式）

1. **遇到操作数（数字或变量）**：直接把它**压入栈中**（Push）。

2. 遇到运算符（+、-、*、/ 等）

   ：

   - 从栈顶**连续弹出（Pop）两个**操作数。
   - **注意顺序**：先弹出的数作为**右操作数**，后弹出的数作为**左操作数**。
   - 把这两个数用该运算符进行计算。
   - 将计算出的**结果重新压入栈中**。

3. **重复上述步骤**，直到表达式的最右端。

4. 扫描结束后，**栈里剩下的唯一一个数字，就是最终的计算结果**。

------

举个直观的例子

我们就用你上一题的表达式结构，假设赋予具体的数字： 中缀表达式：`2 * (3 + 4) - 5` （我们口算知道结果是 `2 * 7 - 5 = 9`） 对应的后缀表达式：**`2 3 4 + \* 5 -`**

我们来看看计算机是如何用栈一步步计算 **`2 3 4 + \* 5 -`** 的：

| 步骤 | 当前扫描到的字符 | 动作            | 当前栈内状态 (从底到顶)        | 说明                                                         |
| :--- | :--------------- | :-------------- | :----------------------------- | :----------------------------------------------------------- |
| 1    | **2** (数字)     | 压栈            | `[2]`                          |                                                              |
| 2    | **3** (数字)     | 压栈            | `[2, 3]`                       |                                                              |
| 3    | **4** (数字)     | 压栈            | `[2, 3, 4]`                    |                                                              |
| 4    | **+** (运算符)   | 弹出4和3，计算  | `[2]` -> 然后压入7 -> `[2, 7]` | 先弹4，再弹3。计算 `3 + 4 = 7`。将7压栈。                    |
| 5    | ***** (运算符)   | 弹出7和2，计算  | `[]` -> 然后压入14 -> `[14]`   | 先弹7，再弹2。计算 `2 * 7 = 14`。将14压栈。                  |
| 6    | **5** (数字)     | 压栈            | `[14, 5]`                      |                                                              |
| 7    | **-** (运算符)   | 弹出5和14，计算 | `[]` -> 然后压入9 -> `[9]`     | **关键！**先弹5作减数，再弹14作被减数。计算 `14 - 5 = 9`。压栈。 |

**扫描结束，栈中剩下的结果是 `9`，这就是最终答案。**
