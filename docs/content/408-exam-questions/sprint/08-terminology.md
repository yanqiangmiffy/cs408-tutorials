# 术语对照表

## 基础术语

| 408 / 教材常用说法 | 常见替代说法 | 说明 |
|-------------------|--------------|------|
| 线性表 | list / linear list | 广义概念，不等于 Python list |
| 顺序存储 | array-based storage | 用连续存储单元保存 |
| 链式存储 | linked storage | 用指针或游标链接 |
| 头结点 | dummy head | 不存实际数据或不参与逻辑数据 |
| 首元结点 | first node | 第一个有效数据结点 |
| 度 | degree | 树中孩子数，图中关联边数 |
| 路径长度 | path length | 通常按边数算 |
| 带权路径长度 | WPL | 只统计叶结点贡献 |

## 树相关

| 教材说法 | LeetCode / 面试说法 | 备注 |
|----------|----------------------|------|
| 二叉排序树 | BST | Binary Search Tree |
| 平衡二叉树 | AVL | 408 更常考 AVL |
| 线索二叉树 | threaded binary tree | 面试较少单独考 |
| 森林 | forest | 多棵互不相交的树 |

## 图相关

| 408 说法 | 常见英文 | 备注 |
|----------|----------|------|
| 邻接矩阵 | adjacency matrix | 稠密图常用 |
| 邻接表 | adjacency list | 稀疏图常用 |
| 入度 / 出度 | indegree / outdegree | 有向图概念 |
| 连通图 | connected graph | 无向图 |
| 强连通图 | strongly connected graph | 有向图 |
| 拓扑排序 | topological sort | 只对 DAG 有定义 |
| 关键路径 | critical path | AOE 网 |

## 排序相关

| 408 说法 | 常见面试说法 | 备注 |
|----------|--------------|------|
| 直接插入排序 | insertion sort | |
| 简单选择排序 | selection sort | |
| 堆排序 | heap sort | |
| 归并排序 | merge sort | 稳定 |
| 基数排序 | radix sort | 非比较排序 |

## LeetCode 题名和 408 模型对照

| LeetCode 常见题 | 408 模型 |
|-----------------|----------|
| Remove Nth Node From End | 双指针链表 |
| Intersection of Two Linked Lists | 公共后缀 / 相交链表 |
| Reorder List | 找中点 + 反转 + 合并 |
| First Missing Positive | 原地哈希 |
| Validate Binary Search Tree | BST 性质判定 |
| Median of Two Sorted Arrays | 二分查找变体 |

## 使用建议

- 刷 LeetCode 时，主动把题目翻译成 408 的知识模型。
- 看王道或教材时，主动给每个概念补一个英文别名，避免以后阅读外部资料卡壳。
