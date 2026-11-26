# 链表

## 1.链表基础操作

### 1.1反转链表

```cpp
//反转单向链表
struct ListNode{
    int val;
    ListNode * next;
};
ListNode * reverselist(ListNode * head){
    ListNode * pre = nullptr;
    ListNode * next = nullptr;
    while(head != nullptr){
        next = head->next;
        head->next = pre;
        pre = head;
        head = next;
    }
    return pre;
}
//反转双向链表
struct listnode{
    int val;
    listnode* next;
    listnode* last;
}
listnode * reversedoublelist(listnode * head){
    listnode * pre = nullptr;
    listnode * next = nullptr;
    while(head != nullptr){
        next = head->next;
        head->next = pre;
        head->last = next;//多加一行，同时处理前后指针
        pre = head;
        head = next;
    }
    return pre;
}
```
