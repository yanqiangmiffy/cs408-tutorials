# 第7章 查找

> 408考研数据结构 · 第7章

## 知识点

| 编号 | 内容 | 文件 |
|------|------|------|
| 7.2 | 顺序查找、折半查找、分块查找 | `7_2_search_algorithms.py` |
| 7.3 | 二叉排序树(BST)与平衡二叉树(AVL) | `7_3_bst_avl.py` |
| 7.5 | 散列表(拉链法/线性探测/平方探测) | `7_5_hash_table.py` |

## 运行

```bash
python 7_search/7_2_search_algorithms.py
python 7_search/7_3_bst_avl.py
python 7_search/7_5_hash_table.py
```

## 考研要点

- **折半查找**: O(log n), 仅适用有序顺序表, 判定树是平衡 BST
- **BST**: 左 < 根 < 右, 中序 = 有序
- **AVL**: 四种旋转 LL/RR/LR/RL
- **散列表**: 除留余数法, 拉链法 vs 开放定址法
- **ASL**: 成功和失败的 ASL 计算
