# Floyd

```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn = 100;
void floyd(int n){
    //枚举每个跳点
    int distance[maxn][maxn] = {0};
    //注意 ： 跳点要最先枚举
    for (int bridge = 0; bridge < n; bridge++){
        for (int i = 0;i<n;i++){
            for (int j = 0;j<n;j++){
                // i -> …… bridge …… -> j
                // distance[i][j] 能不能缩短
                if (distance[i][bridge] != INT_MAX && distance[bridge][j] != INT_MAX && distance[i][j] > distance[i][bridge] + distance[bridge][j]){
                    distance[i][j] = distance[i][bridge] + distance[bridge][j];
                }
            }
        }
    }
}
```
