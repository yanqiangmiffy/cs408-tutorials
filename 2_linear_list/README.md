# 第2章 线性表

> 408考研数据结构 · 第2章

## 知识点

| 编号 | 内容 | 文件 |
|------|------|------|
| 2.2 | 顺序表的定义、插入、删除、查找 | `2_2_sequential_list.py` |
| 2.3.1-2.3.2 | 单链表的定义、插入、删除、查找、建立 | `2_3_singly_linked_list.py` |
| 2.3.3 | 双链表 | `2_3_doubly_linked_list.py` |
| 2.3.4 | 循环链表(单/双) | `2_3_circular_linked_list.py` |
| 2.3.5 | 静态链表 | `2_3_static_linked_list.py` |

## 运行

```bash
python 2_linear_list/2_2_sequential_list.py
python 2_linear_list/2_3_singly_linked_list.py
python 2_linear_list/2_3_doubly_linked_list.py
python 2_linear_list/2_3_circular_linked_list.py
python 2_linear_list/2_3_static_linked_list.py
```

## 考研要点

### 顺序表 vs 链表

| 特性 | 顺序表 | 链表 |
|------|--------|------|
| 存取方式 | 随机存取 O(1) | 顺序存取 O(n) |
| 插入/删除 | O(n) 需移动元素 | O(1) 只改指针 |
| 存储密度 | 高 (无指针开销) | 低 (有指针域) |
| 空间分配 | 预先分配 | 动态分配 |

### 选择建议
- **表长可预估、查询多** → 顺序表
- **频繁插入删除、表长不确定** → 链表
