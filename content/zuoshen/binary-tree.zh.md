# 二叉树
## 1.二叉树及其三种序的实现
### 1.1 递归实现
时间复杂度：O(n)
空间复杂度：O(h) h是树的高度
* 先序遍历：任何一颗子树都满足：*根 左 右* 的顺序
* 中序遍历：任何一颗子树都满足：*左 根 右* 的顺序
* 后序遍历：任何一颗子树都满足：*左 右 根* 的顺序
```cpp
struct Treenode{
    int val;
    Treenode* left;
    Treenode* right;
    Treenode(int x):val(x), left(NULL), right(NULL) {}
};
class Solution{
public:
    vector<int> res;
    void preOrder(Treenode* root){
        if (root == NULL){
            return;
        }
        res.push_back(root->val);
        preOrder(root->left);
        preOrder(root->right);
    }
    vector<int> preOrderTravel(Treenode * root){
        preOrder(root);
        return res;
    }
    void inOrder(Treenode* root){
        if(root == NULL){
            return;
        }
        inOrder(root->left);
        res.push_back(root->val);
        inOrder(root->right);
    }
    vector<int> inOrderTravel(Treenode * root){
        inOrder(root);
        return res;
    }
    void posOrder(Treenode * root){
        if (root == NULL) return;
        posOrder(root->left);
        posOrder(root->right);
        res.push_back(root->val);
    }
    vector<int> posOrderTravel(Treenode * root){
        posOrder(root);
        return res;
    }
    //终极理解递归序和先中后序
    void f(Treenode * root){
        if (root == NULL) return;
        //1
        f(root->left);
        //2
        f(root->right);
        //3
    }
    //递归序：1，2，4，4，4，2，5，5，5，2，1，3，6，6，6，3，7，7，7，3，1
    //先序   1，2，4，        5，            3，6，        7
    //中序            4，   2，   5，     1，      6，   3，   7
    //后序               4，         5，2，           6，        7，3，1
};
```
### 1.2 非递归实现
时间复杂度：O(n)
空间复杂度：O(h) h是树的高度
```cpp
struct Treenode{
    int val;
    Treenode* left;
    Treenode* right;
    Treenode(int x):val(x), left(NULL), right(NULL) {}
};
class Solution{
public:
    void preOrder(Treenode * root){
        if (root != NULL){
            stack<Treenode*> stk;
            stk.push(root);
            while(!stk.empty()){
                Treenode* root = stk.top();
                stk.pop();
                cout << root->val << ' ';
                if (root->right != NULL){
                    stk.push(root->right);
                }
                if (root->left != NULL){
                    stk.push(root->left);
                }
            }
        }
    }
    //中序遍历：
    //1）子树左边界进栈（完全进栈）
    //2）栈弹出节点打印，节点右树重复1）
    //3）没子树且栈空
    void inOrder(Treenode * root){
        if (root != NULL){
            stack<Treenode*> stk;
            while(!stk.empty() || root != NULL){
                if (root != NULL){
                    stk.push(root);
                    root = root->left;
                }
                //到了左边界了
                else{
                    root = stk.top();
                    stk.pop();
                    cout << root->val << " ";
                    root = root->right;//右树重复1）
                }
            }
        }
    }
    //先序：  中 左 右
    //先序' : 中 右 左
    //后序：  左 右 中
    //那么后序我只需要用两个栈即可
    void posOrder1(Treenode * root){
        if (root != NULL){
            stack<Treenode *> stk;
            stack<Treenode *> collect;
            stk.push(root);
            while(!stk.empty()){
                root = stk.top();
                stk.pop();
                collect.push(root);
                if(root->left){
                    stk.push(root->left);
                }
                if(root->right){
                    stk.push(root->right);
                }
            }
            while(!collect.empty()){
                root = collect.top();
                collect.pop();
                cout << root->val << ' ';
            }
        }
    }
    //额外空间复杂度O(n),较高
    //那么我如果用一个栈来实现呢？
    //需要引入一个标记h
    void posOrder2(Treenode * h){
        if (h != NULL){
            stack<Treenode*> stk;
            stk.push(h);
            //如果始终没有打印过节点，h就一直是头节点
            //一旦打印过节点，h就变成打印节点
            //之后h的含义：上一次打印的节点
            while(!stk.empty()){
                Treenode * cur = stk.top();
                if (cur->left != NULL && h != cur->left && h != cur->right){
                    //有左树且左树没处理过
                    stk.push(cur->left);
                }
                else if(cur->right != NULL && h != cur->right){
                    //有右树且右树没处理过
                    stk.push(cur->right);
                }
                else{
                    //左树、右树没有或者都处理过了
                    cout << cur->val << ' ';
                    h = stk.top();
                    stk.pop();
                }
            }
        }
    }
};
```
## 2.二叉树高频题目（不含树形dp）
### T1 [二叉树的层序遍历 leetcode No.102](https://leetcode.cn/problems/binary-tree-level-order-traversal/description/)
```cpp
vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        if(root != NULL){
            queue<TreeNode*> que;
            que.push(root);
            while(!que.empty()){
                vector<int> tmp;
                int size = que.size();//很重要的一步，必须用变量size记录当前队列大小，因为如果直接使用que.size(),每次弹出后size会变，达不到按层遍历的效果
                for (int i = 0;i<size;i++){
                    TreeNode* cur = que.front();
                    que.pop();
                    tmp.push_back(cur->val);
                    if (cur->left) que.push(cur->left);
                    if (cur->right) que.push(cur->right);
                }
                ans.push_back(tmp);
            }
        }
        return ans;
    }
```
### T2 [二叉树的锯齿形层序遍历 leetcode No.103](https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/description/)
```cpp
//version 1
//使用数组模拟队列
vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        if (root != NULL){
            int l = 0, r = 0;
            TreeNode* que[2001];
            que[r++] = root;
            bool flag = false;//reverse标志
            //flag == false 左->右， l->r-1,收集size个
            //flag == true  右->左， r-1->l,收集size个
            while(l < r){
                int size = r - l;
                vector<int> list;
                for(int i = flag ? (r-1) : l, j = flag ? -1 : 1, k = 0; k<size;k++,i+=j){
                    TreeNode * cur = que[i];
                    list.push_back(cur->val);
                }
                for (int i = 0;i<size;i++){
                    TreeNode * cur = que[l++];
                    if (cur->left){
                        que[r++] = cur->left;
                    }
                    if (cur->right){
                        que[r++] = cur->right;
                    }
                }
                ans.push_back(list);
                list.clear();
                flag = !flag;
            }
        }
        return ans;
    }
//version 2
//使用双端队列
vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        deque<TreeNode*> deque;
        if(root != NULL) deque.push_back(root);
        while(!deque.empty()){
            //打印奇数层
            vector<int> list;
            for (int i = deque.size();i>0;i--){
                //left->right
                TreeNode* cur = deque.front();
                deque.pop_front();
                list.push_back(cur->val);
                if(cur->left) deque.push_back(cur->left);
                if(cur->right) deque.push_back(cur->right);
            }
            ans.push_back(list);
            list.clear();
            if(deque.empty()) break;//没有偶数层提前退出
            //打印偶数层
            for(int i = deque.size();i>0;i--){
                //right->left
                TreeNode* cur = deque.back();
                deque.pop_back();
                list.push_back(cur->val);
                if(cur->right) deque.push_front(cur->right);
                if(cur->left) deque.push_front(cur->left);
            }
            ans.push_back(list);
            list.clear();
        }
        return ans;
    }
```
### T3
