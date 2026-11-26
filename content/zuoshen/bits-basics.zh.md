# 1.二进制和位运算

## 1.1 补码

正数：原码

负数：正数**取反加一或减一取反**

注意比如二进制是4位，那么可表示-8 ~ -1，0 ~ 7，不能表示8

**相反数**：同样取反加一或减一取反相当于得到了相反数

为什么要这样设计？

可以使用一套加法逻辑，不需要**条件转移**（-5+2 和 3 + 2 的逻辑一致，即便溢出取反会变0）

**溢出**：自己确保调用的结果不会溢出，计算机不会给你报错

打印一个int类型的数字，32位进制的状态

```cpp
void printBinary(int num){
    for (int i = 31; i>= 0;i--){
        cout << ((num & (1 << i) == 0) ? "0" : "1");
    }
}
```

打印一个long long 类型的数字，64位进制的状态

```cpp
void printBinary(long long num){
    for (int i = 63;i>=0;i--){
        cout << ((num & (1LL << i) == 0) ? "0" : "1");//注意1必须加后缀，要不然会溢出
    }
}
```

## 1.2 异或运算的骚操作

先来玩一个好玩的问题:

袋子里一共a个白球，b个黑球，每次从袋子里拿2个球，每个球被拿出的概率机会均等

如果拿出的是2个白球或者2个黑球，那么就往袋子里重新放入1个白球

如果拿出的是1个黑球和1个白球，那么就往袋子里重新放入1个黑球

那么最终袋子里一定会只剩1个球，请问最终的球是黑的概率是多少？用a和b来表达这个概率

答案:

如果黑球的数量是偶数,最终的球是黑球的概率是0%

如果黑球的数量是奇数,最终的球是黑的概率是100%

完全和白球的数量无关

### 异或运算的性质

1. 异或运算就是无进位相加
2. 异或运算满足交换律和结合律
3. 0^n=n, n^n=0
4. a^b=c ->  a = b ^ c, b = a ^ c

那么我们回到刚才的问题,把白球看成0, 黑球看成1,那么0 ^ 1 = 1, 1 ^ 1 = 0, 0^ 0 = 0,那么a个0和b个1的异或和就是最终答案

### 交换两个数

```cpp
int a = 0, b = 10;
a = a ^ b;
b = a ^ b;
a = a ^ b;
//a = 甲, b = 乙, a = 甲 ^ 乙, b = (甲 ^ 乙) ^ 乙 = 甲 ^ 0 = 甲, a = (甲 ^ 乙) ^ 甲 = 0 ^ 乙 = 乙
```

### 不用任何判断语句和比较操作,返回两个数的最大值

```cpp
int flip(int n){
    return n ^ 1;
}
//非负数返回1,负数返回0
int sign(int n){
    return flip((n >> 31) & 1);
}
//有溢出风险的实现
int getmax1(int a, int b){
    int c = a - b;
    //c非负,returna->1, returnb->0
    //c负数,returna->0, returnb->1
    int returna = sign(c);
    int returnb = flip(returnA);
    return returna * a + returnb * b;
}
//没有任何问题的实现
int getmax2(int a, int b){
    //c可能是溢出的
    int c = a - b;
    int sa = sign(a);
    int sb = sign(b);
    int sc = sign(c);
    //判断a和b的符号是不是一样的,如果不一样是1,一样是0
    int diffab = sa ^ sb;
    int sameab = flip(diffab);
    //a和b符号不一样,且a非负||a和b的符号一样,且c非负
    int returna = diffab * sa + sameab * sc;
    int returnb = flip(returna);
    return returna * a + returnb * b;
}
```

### 找到缺失的数字

```cpp
int missingnum(vector<int> & nums){
    int eorall = 0, eorhas = 0;
    for (int i = 0;i<nums.size();i++){
        eorall ^= i;
        eorhas ^= nums[i];
    }
    eorall ^= nums.size();
    return eorall ^ eorhas;
}
```

### 只出现一次的数字

给你一个 **非空** 整数数组 `nums` ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。



**示例 1 ：**

**输入：**nums = [2,2,1]

**输出：**1

**示例 2 ：**

**输入：**nums = [4,1,2,1,2]

**输出：**4

**示例 3 ：**

**输入：**nums = [1]

**输出：**1



**提示：**

- `1 <= nums.length <= 3 * 104`
- `-3 * 104 <= nums[i] <= 3 * 104`
- 除了某个元素只出现一次以外，其余每个元素均出现两次。

```cpp
int singlenum(vector<int> & nums){
	int eor = 0;
    for (int num : nums){
        eor ^= num;
    }
    return eor;
}
```

### 提取出**一个正整数在二进制表示下，最低位的 `1` 以及它后面的 `0` 所构成的数值**

```cpp
int lowbit(int x){
    return x & (-x);
}
//树状数组中常用
```

### 数组中有2种数出现了奇数次,其他都是偶数次

给你一个整数数组 `nums`，其中恰好有两个元素只出现一次，其余所有元素均出现两次。 找出只出现一次的那两个元素。你可以按 **任意顺序** 返回答案。

你必须设计并实现线性时间复杂度的算法且仅使用常量额外空间来解决此问题。



**示例 1：**

```
输入：nums = [1,2,1,3,2,5]
输出：[3,5]
解释：[5, 3] 也是有效的答案。
```

**示例 2：**

```
输入：nums = [-1,0]
输出：[-1,0]
```

**示例 3：**

```
输入：nums = [0,1]
输出：[1,0]
```



**提示：**

- `2 <= nums.length <= 3 * 104`
- `-231 <= nums[i] <= 231 - 1`
- 除两个只出现一次的整数外，`nums` 中的其他数字都出现两次

```cpp
int lowbit(int x){
    return x & (-x);
}
int singlenum(vector<int> & nums){
    int eor1 = 0;
    for (int num : nums){
        eor1 ^= num;
    }
    //eor1 = a ^ b
    int rightone = lowbit(eor1);
    int eor2 = 0;
    //借助rightone一定可以分开a和b
    for (int num : nums){
        if (num & rightone == 0){
            eor2 ^= num;
        }
    }
    return {eor2, eor2 ^ eor1};
}
```

### 异或思想但不完全使用异或

已知数组中只有1种数出现次数少于m次,其他数都出现了m次,返回出现次数小于m次的那种数

```cpp
int find(vector<int> arr, int m){
    //cnt[i] i位上有多少个1
    int cnt[32] = {0};
    for (int num : arr){
        for (int i = 0;i<32;i++){
            cnt[i] += (num >> i) & 1;
        }
	}
    int ans = 0;
    for (int i = 0;i<32;i++){
        if (cnt[i] % m != 0){
            ans |= 1 << i;
		}
    }
    return ans;
}
```

## 1.3 位运算的骚操作

### 判断一个整数是不是2的幂

2的幂的二进制里只有一个1

```cpp
int lowbit(int x){
    return x & (-x);
}
bool judge(int x){
    return x > 0 && x == (lowbit(x)) ;
}
```

### 判断一个整数是不是3的幂

```cpp
//如果一个数字是3的幂,那么它只有3一个质数因子
//1162261467是int型范围内最大的3的幂,3^19
bool judge(int x){
    return x > 0 && 1162261467 % x == 0;
}
```

### 返回大于等于n的最小的2的幂

```cpp
int near2power(int x){
    if (n <= 0){
        return 1;
    }
    n = (unsigned int)n - 1;//-1是因为需要返回大于等于n的最小幂,否则会得到2 * n;
    n = n >> 1;
    n = n >> 2;
    n = n >> 4;
    n = n >> 8;
    n = n >> 16;
    return n + 1;
}
```

### 返回[left, right]所有数字 & 的结果

```cpp
int AND(int left, int right){
    while (left < right){
        right -= (right & -right);
    }
    return right;
}
```
