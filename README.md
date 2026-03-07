# 408考研 · 数据结构 Python 实现

> 王道408数据结构全部章节的 Python 代码实现，每个知识点配有详细注释、运行演示和考研要点速记。

## 📁 目录结构

```
cs408-tutorials/
├── 1_introduction/          # 第1章 绪论
│   ├── 1_1_basic_concepts.py        # 数据结构基本概念、三要素
│   ├── 1_2_time_complexity.py       # 时间复杂度分析
│   └── 1_3_space_complexity.py      # 空间复杂度分析
│
├── 2_linear_list/           # 第2章 线性表
│   ├── 2_2_sequential_list.py       # 顺序表
│   ├── 2_3_singly_linked_list.py    # 单链表
│   ├── 2_3_doubly_linked_list.py    # 双链表
│   ├── 2_3_circular_linked_list.py  # 循环链表
│   └── 2_3_static_linked_list.py    # 静态链表
│
├── 3_stack_queue/           # 第3章 栈、队列和数组
│   ├── 3_1_stack.py                 # 栈(顺序栈/链栈/共享栈)
│   ├── 3_2_queue.py                 # 队列(循环队列/链队列/双端队列)
│   ├── 3_3_stack_applications.py    # 括号匹配、表达式求值
│   └── 3_4_matrix_compression.py    # 特殊矩阵压缩存储
│
├── 4_string/                # 第4章 串
│   └── 4_1_pattern_matching.py      # 朴素匹配、KMP算法
│
├── 5_tree/                  # 第5章 树与二叉树
│   ├── 5_3_binary_tree_traversal.py # 二叉树遍历、序列构造
│   ├── 5_3_threaded_binary_tree.py  # 线索二叉树
│   ├── 5_5_huffman_tree.py          # 哈夫曼树与编码
│   └── 5_5_union_find.py           # 并查集
│
├── 6_graph/                 # 第6章 图
│   ├── 6_2_graph_storage.py         # 邻接矩阵、邻接表
│   ├── 6_3_bfs_dfs.py              # BFS、DFS 遍历
│   ├── 6_4_mst.py                  # 最小生成树(Prim/Kruskal)
│   ├── 6_4_shortest_path.py        # 最短路径(Dijkstra/Floyd)
│   └── 6_4_topo_critical_path.py   # 拓扑排序、关键路径
│
├── 7_search/                # 第7章 查找
│   ├── 7_2_search_algorithms.py     # 顺序/折半/分块查找
│   ├── 7_3_bst_avl.py              # BST、AVL 树
│   └── 7_5_hash_table.py           # 散列表
│
└── 8_sorting/               # 第8章 排序
    ├── bubble_sort.py               # 冒泡排序
    ├── insertion_sort.py            # 直接插入排序
    ├── selection_sort.py            # 简单选择排序
    ├── shell_sort.py                # 希尔排序
    ├── quick_sort.py                # 快速排序
    ├── merge_sort.py                # 归并排序
    ├── heap_sort.py                 # 堆排序
    ├── counting_sort.py             # 计数排序
    └── radix_sort.py                # 基数排序
```

## 🚀 使用方法

每个 Python 文件都可以直接运行：

```bash
python 1_introduction/1_1_basic_concepts.py
python 4_string/4_1_pattern_matching.py
python 6_graph/6_4_shortest_path.py
# ...
```

## 📝 代码风格

每个文件包含：
- 📝 顶部文档注释（算法思想、复杂度、考研要点）
- ⚡ 标准实现函数
- 🔍 带详细输出的 verbose 演示版本
- ✅ 测试用例和运行示例
- 📌 考研要点速记
