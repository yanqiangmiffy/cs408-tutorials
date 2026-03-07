# 第5章 树与二叉树

> 408考研数据结构 · 第5章

## 知识点

| 编号 | 内容 | 文件 |
|------|------|------|
| 5.3 | 二叉树的遍历(先/中/后/层序) + 由序列构造 | `5_3_binary_tree_traversal.py` |
| 5.3.2 | 线索二叉树 | `5_3_threaded_binary_tree.py` |
| 5.5.1 | 哈夫曼树与哈夫曼编码 | `5_5_huffman_tree.py` |
| 5.5.2 | 并查集 | `5_5_union_find.py` |

## 运行

```bash
python 5_tree/5_3_binary_tree_traversal.py
python 5_tree/5_3_threaded_binary_tree.py
python 5_tree/5_5_huffman_tree.py
python 5_tree/5_5_union_find.py
```

## 考研要点

- **遍历**: 先序(根左右) 中序(左根右) 后序(左右根)
- **序列构造**: 中序 + (先序/后序/层序) → 唯一确定
- **线索化**: 利用 n+1 个空指针域存前驱后继
- **哈夫曼**: WPL 最小, n 个叶子 → 2n-1 个节点
- **并查集**: Find + Union, 按秩合并 + 路径压缩
