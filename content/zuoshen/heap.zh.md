实现勘误：下面保留了笔记中的两种建堆写法。第一种写法里的 `HeapInsert(arr, arr[i])` 应传下标 `i`，写成 `HeapInsert(arr, i)`。第二种写法从最后一个非叶节点向上调整。

# 堆结构和堆排序

```cpp
#include <bits/stdc++.h>
using namespace std;
//arr[i] = x, x是新来的，往上看，直到不比父亲大，或者来到0位置（顶）
void HeapInsert(vector<int> & arr, int i){
	// i -> father : (i-1)/2;
	while (arr[i] > arr[(i-1)/2]){//0位置时两边都是0，本身也不比父亲大
		swap(arr[i], arr[(i-1) / 2]);
		i = (i - 1) / 2;
	}
}
//i 位置的数变小了，又想维持大根堆的结构
//向下调整大根堆
//当前堆的大小为size
void heapify(vector<int> & arr, int i, int size){
	int l = 2 * i + 1;
	while (l < size){
		//有左孩子
		//右孩子 ： l+1
		// 评选最强的孩子，是哪个下标的孩子
		int best = l + 1 < size && arr[l + 1] > arr[l] ? (l + 1) : l;
		// 上面已经评选了最强的孩子，接下来，当前的数，和最强的孩子之前，最强下标是谁
		best = arr[best] > arr[i] ? best : i;
		if (best == i){
			break;
		}
		swap(arr[best], arr[i]);
		i = best;//退下来了
		l = 2 * i + 1;
	}
}
//从顶到底建立大顶堆， O(n * logn)
//依次弹出堆内最大值并排好序，O(n * logn)
//整体时间复杂度O(n * log n)
void heapsort1(vector<int> & arr){
    int n = arr.size();
    for (int i = 0;i<n;i++)
    {
        HeapInsert(arr, arr[i]);
    }
    int size = n;
    while (size > 1){
        swap(arr[0], arr[--size]);
        heapify(arr, 0, size);
    }
}
//从底到顶建堆，O(n)
void heapsort2(vector<int> & arr){
    int n = arr.size();
    for (int i = n/2; i >=0 ;i--){
        heapify(arr, i, n);
    }
    int size = n;
    while (size > 1){
        swap(arr[0], arr[--size]);
        heapify(arr, 0, size);
    }
}


```
