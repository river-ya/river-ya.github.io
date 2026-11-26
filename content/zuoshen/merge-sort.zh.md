# 归并排序

```cpp
const int maxn = 1000;
int arr[maxn];
int help[maxn];//辅助数组
int n;
//归并排序递归版
void merge(int l, int m, int r){
    int i = l;
    //[l …… m] [m+1 …… r]
    int a = l, b = m + 1;
    while (a <= m && b <= r){
        help[i++] = arr[a] <= arr[b] ? arr[a++] : arr[b++];
    }
    // 左侧指针，右侧指针， 必有一个越界，另一个不越界
    while (a <= m){
        help[i++] = arr[a++];
    }
    while (b <= r){
        help[i++] = arr[b++];
    }
    for (i = l; i <= r; i++){
        arr[i] = help[i];
    }
}
void mergesort1(int l, int r){
    if (l == r) return;
    int m = l + (r - l) / 2;
    mergesort1(l, m);
    mergesort1(m + 1, r);
    merge(l, m, r);
}
```
