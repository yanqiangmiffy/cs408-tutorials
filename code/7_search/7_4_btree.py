"""
7.4 B树和B+树 (B-tree and B+ Tree) - 408考研数据结构

本文件包含B树和B+树的完整Python实现，包括：
1. B树的插入、查找、删除操作
2. B+树的插入、查找操作
3. 详细的节点分裂和提升操作
4. 手写过程模拟和测试用例

作者: 408考研数据结构复习
"""

from typing import Optional, List, Tuple


# ==================== B树 ====================

class BTreeNode:
    """B树节点"""

    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys = []  # 关键字列表，最多 m-1 个
        self.children = []  # 子节点列表，最多 m 个

    def __repr__(self):
        return f"BTreeNode(keys={self.keys}, is_leaf={self.is_leaf})"


class BTree:
    """B树 - 多路平衡查找树

    性质：
    - 树中每个结点至多有 m 个孩子
    - 除根结点和叶结点外，每个结点至少有 ⌈m/2⌉ 个孩子
    - 若根结点不是叶结点，则至少有两个孩子
    - 所有叶结点在同一层
    - 每个非叶结点有 n 个关键字和 n+1 个孩子

    时间复杂度：O(logₘn)
    """

    def __init__(self, order: int = 3):
        """
        初始化B树

        Args:
            order: B树的阶数 m，通常为3或更大
        """
        self.order = order  # m路树
        self.root = None
        self.min_keys = (order - 1) // 2  # 最小关键字数（非根节点）
        self.max_keys = order - 1  # 最大关键字数

    def search(self, key: int) -> bool:
        """B树查找 - O(logₘn)"""
        return self._search(self.root, key)

    def _search(self, node: Optional[BTreeNode], key: int) -> bool:
        if not node:
            return False

        # 在当前结点中查找
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # 找到关键字
        if i < len(node.keys) and key == node.keys[i]:
            return True

        # 递归搜索子结点
        if not node.is_leaf:
            return self._search(node.children[i], key)

        return False

    def insert(self, key: int) -> None:
        """B树插入"""
        if not self.root:
            self.root = BTreeNode(True)
            self.root.keys.append(key)
            return

        # 递归插入
        overflow_key, overflow_child = self._insert(self.root, key)

        # 如果根结点溢出，需要分裂
        if overflow_key is not None:
            new_root = BTreeNode(False)
            new_root.keys.append(overflow_key)
            new_root.children.append(self.root)
            new_root.children.append(overflow_child)
            self.root = new_root

    def _insert(self, node: BTreeNode, key: int) -> Tuple[Optional[int], Optional[BTreeNode]]:
        """递归插入，返回(溢出的关键字, 新的右子结点)"""
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # 如果关键字已存在，直接返回
        if i < len(node.keys) and key == node.keys[i]:
            return None, None

        # 叶结点：直接插入
        if node.is_leaf:
            node.keys.insert(i, key)
        else:
            # 非叶结点：递归插入到子结点
            overflow_key, overflow_child = self._insert(node.children[i], key)

            # 子结点没有溢出
            if overflow_key is None:
                return None, None

            # 子结点溢出，插入溢出的关键字
            node.keys.insert(i, overflow_key)
            node.children.insert(i + 1, overflow_child)

        # 检查是否溢出
        if len(node.keys) > self.max_keys:
            return self._split(node)

        return None, None

    def _split(self, node: BTreeNode) -> Tuple[int, BTreeNode]:
        """分裂结点，返回(提升的关键字, 新的右子结点)"""
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]

        # 创建新的右结点
        new_node = BTreeNode(node.is_leaf)
        new_node.keys = node.keys[mid_index + 1:]
        if not node.is_leaf:
            new_node.children = node.children[mid_index + 1:]

        # 更新原结点
        node.keys = node.keys[:mid_index]
        if not node.is_leaf:
            node.children = node.children[:mid_index + 1]

        return mid_key, new_node

    def delete(self, key: int) -> bool:
        """B树删除（简化版本 - 适合408考研演示）"""
        # 简化版：重新构建树（实际考试时重点在手算过程）
        traversal = self.inorder_traversal()
        if key not in traversal:
            return False

        traversal.remove(key)
        self.root = None
        for k in traversal:
            self.insert(k)
        return True

    def display(self, node: Optional[BTreeNode] = None, level: int = 0):
        """打印B树结构"""
        if node is None:
            node = self.root

        indent = "  " * level
        print(f"{indent}Keys: {node.keys}")
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                print(f"{indent}  Child {i}:")
                self.display(child, level + 2)

    def inorder_traversal(self, node: Optional[BTreeNode] = None, result: Optional[List[int]] = None) -> List[int]:
        """中序遍历B树"""
        if node is None:
            node = self.root
        if result is None:
            result = []

        i = 0
        if not node.is_leaf:
            while i < len(node.keys):
                self.inorder_traversal(node.children[i], result)
                result.append(node.keys[i])
                i += 1
            self.inorder_traversal(node.children[i], result)
        else:
            result.extend(node.keys)

        return result


# ==================== B+树 ====================

class BPlusTreeNode:
    """B+树节点"""

    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys = []  # 关键字列表，最多 m-1 个
        self.children = []  # 子节点列表，最多 m 个
        self.next = None  # 叶子结点的链表指针

    def __repr__(self):
        return f"BPlusTreeNode(keys={self.keys}, is_leaf={self.is_leaf})"


class BPlusTree:
    """B+树 - B树的变体

    与B树的区别：
    - 所有关键字都出现在叶子结点
    - 叶子结点之间有链表指针，便于范围查询
    - 内部结点只用于索引，包含指向下一层的指针

    时间复杂度：O(logₘn)
    """

    def __init__(self, order: int = 3):
        """
        初始化B+树

        Args:
            order: B+树的阶数 m
        """
        self.order = order
        self.root = None
        self.min_keys = (order - 1) // 2  # 最小关键字数
        self.max_keys = order - 1  # 最大关键字数
        self.leaf_head = None  # 叶子链表头

    def search(self, key: int) -> bool:
        """B+树查找 - O(logₘn)"""
        node = self._find_leaf(self.root, key)
        if not node:
            return False

        for k in node.keys:
            if k == key:
                return True
        return False

    def _find_leaf(self, node: Optional[BPlusTreeNode], key: int) -> Optional[BPlusTreeNode]:
        """找到包含key的叶子结点"""
        if not node:
            return None

        if node.is_leaf:
            return node

        i = 0
        while i < len(node.keys) and key >= node.keys[i]:
            i += 1

        return self._find_leaf(node.children[i], key)

    def insert(self, key: int) -> None:
        """B+树插入"""
        if not self.root:
            self.root = BPlusTreeNode(True)
            self.root.keys.append(key)
            self.leaf_head = self.root
            return

        # 找到叶子结点
        leaf = self._find_leaf(self.root, key)

        # 检查关键字是否已存在
        if key in leaf.keys:
            return

        # 插入关键字
        i = 0
        while i < len(leaf.keys) and key > leaf.keys[i]:
            i += 1
        leaf.keys.insert(i, key)

        # 检查叶子结点是否溢出
        if len(leaf.keys) > self.max_keys:
            self._insert_node(self.root, key)

    def _insert_node(self, node: BPlusTreeNode, key: int) -> Tuple[Optional[int], Optional[BPlusTreeNode]]:
        """递归插入，处理溢出"""
        if node.is_leaf:
            return self._split_leaf(node)

        # 找到子结点
        i = 0
        while i < len(node.keys) and key >= node.keys[i]:
            i += 1

        # 递归处理子结点
        overflow_key, new_node = self._insert_node(node.children[i], key)

        # 没有溢出
        if overflow_key is None:
            return None, None

        # 插入溢出的关键字和新的子结点
        node.keys.insert(i, overflow_key)
        node.children.insert(i + 1, new_node)

        # 检查当前结点是否溢出
        if len(node.keys) > self.max_keys:
            return self._split_internal(node)

        return None, None

    def _split_leaf(self, leaf: BPlusTreeNode) -> Tuple[int, BPlusTreeNode]:
        """分裂叶子结点"""
        mid_index = (len(leaf.keys) + 1) // 2
        mid_key = leaf.keys[mid_index]

        # 创建新的叶子结点
        new_leaf = BPlusTreeNode(True)
        new_leaf.keys = leaf.keys[mid_index:]

        # 更新原叶子结点
        leaf.keys = leaf.keys[:mid_index]

        # 更新叶子链表
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        return mid_key, new_leaf

    def _split_internal(self, node: BPlusTreeNode) -> Tuple[int, BPlusTreeNode]:
        """分裂内部结点"""
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]

        # 创建新的内部结点
        new_node = BPlusTreeNode(False)
        new_node.keys = node.keys[mid_index + 1:]
        new_node.children = node.children[mid_index + 1:]

        # 更新原结点
        node.keys = node.keys[:mid_index]
        node.children = node.children[:mid_index + 1]

        return mid_key, new_node

    def delete(self, key: int) -> bool:
        """B+树删除（简化版本）"""
        if not self.root:
            return False

        leaf = self._find_leaf(self.root, key)

        if key not in leaf.keys:
            return False

        leaf.keys.remove(key)

        # 处理下溢（简化）
        # 实际实现需要处理借关键字和合并

        # 如果根结点为空且不是叶子结点
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]

        return True

    def range_search(self, start: int, end: int) -> List[int]:
        """范围查询 [start, end]"""
        result = []
        leaf = self._find_leaf(self.root, start)

        while leaf is not None and len(leaf.keys) > 0:
            for k in leaf.keys:
                if start <= k <= end:
                    result.append(k)
                elif k > end:
                    return result
            leaf = leaf.next

        return result

    def display(self, node: Optional[BPlusTreeNode] = None, level: int = 0):
        """打印B+树结构"""
        if node is None:
            node = self.root

        indent = "  " * level
        if node.is_leaf:
            print(f"{indent}Leaf: {node.keys}")
        else:
            print(f"{indent}Internal: {node.keys}")
            for i, child in enumerate(node.children):
                print(f"{indent}  Child {i}:")
                self.display(child, level + 2)

    def display_leaves(self):
        """打印叶子链表"""
        print("Leaf chain:")
        leaf = self.leaf_head
        while leaf:
            print(f"  {leaf.keys}", end=" -> " if leaf.next else "\n")
            leaf = leaf.next

    def inorder_traversal(self) -> List[int]:
        """中序遍历B+树"""
        result = []
        leaf = self.leaf_head
        while leaf:
            result.extend(leaf.keys)
            leaf = leaf.next
        return result


# ==================== 测试函数 ====================

def test_btree():
    """测试B树"""
    print("=" * 50)
    print("B树测试")
    print("=" * 50)

    tree = BTree(order=3)
    keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    print("\n插入关键字:", keys)
    for key in keys:
        tree.insert(key)
        print(f"插入 {key} 后:")
        tree.display()

    print("\n中序遍历:", tree.inorder_traversal())

    print("\n查找测试:")
    for key in [10, 30, 50, 100]:
        print(f"查找 {key}: {'找到' if tree.search(key) else '未找到'}")

    print("\n删除测试:")
    delete_keys = [30, 40, 50]
    for key in delete_keys:
        print(f"\n删除 {key} 后:")
        tree.delete(key)
        tree.display()
        print("中序遍历:", tree.inorder_traversal())


def test_bplustree():
    """测试B+树"""
    print("\n" + "=" * 50)
    print("B+树测试")
    print("=" * 50)

    tree = BPlusTree(order=3)
    keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    print("\n插入关键字:", keys)
    for key in keys:
        tree.insert(key)
        print(f"插入 {key} 后:")
        tree.display()

    print("\n叶子链表:")
    tree.display_leaves()

    print("\n中序遍历:", tree.inorder_traversal())

    print("\n查找测试:")
    for key in [10, 30, 50, 100]:
        print(f"查找 {key}: {'找到' if tree.search(key) else '未找到'}")

    print("\n范围查询 [20, 50]:", tree.range_search(20, 50))
    print("范围查询 [35, 70]:", tree.range_search(35, 70))


def demonstrate_btree_search():
    """演示B树查找手写过程"""
    print("\n" + "=" * 50)
    print("B树查找手写过程演示")
    print("=" * 50)

    print("\n构建3阶B树，插入: [50, 30, 70, 20, 40, 60, 80]")
    tree = BTree(order=3)
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key)

    print("\nB树结构:")
    tree.display()

    print("\n查找 40:")
    print("第1层: 根[50], 40 < 50 -> 查找左子树")
    print("第2层: 结点[30, 40], 40 == 40 找到!")
    print(f"实际结果: {'找到' if tree.search(40) else '未找到'}")

    print("\n查找 60:")
    print("第1层: 根[50], 60 > 50 -> 查找右子树")
    print("第2层: 结点[60, 70, 80], 60 == 60 找到!")
    print(f"实际结果: {'找到' if tree.search(60) else '未找到'}")

    print("\n查找 25:")
    print("第1层: 根[50], 25 < 50 -> 查找左子树")
    print("第2层: 结点[20, 30, 40], 25 不在列表中 未找到")
    print(f"实际结果: {'找到' if tree.search(25) else '未找到'}")


def demonstrate_bplustree_search():
    """演示B+树查找手写过程"""
    print("\n" + "=" * 50)
    print("B+树查找手写过程演示")
    print("=" * 50)

    print("\n构建3阶B+树，插入: [50, 30, 70, 20, 40, 60, 80]")
    tree = BPlusTree(order=3)
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key)

    print("\nB+树结构:")
    tree.display()

    print("\n叶子链表:")
    tree.display_leaves()

    print("\n查找 40:")
    print("第1层: 根[50], 40 < 50 -> 查找左子树")
    print("第2层: 叶子结点[20, 30, 40], 40 == 40 找到!")
    print(f"实际结果: {'找到' if tree.search(40) else '未找到'}")

    print("\n查找 65:")
    print("第1层: 根[50], 65 > 50 -> 查找右子树")
    print("第2层: 叶子结点[60, 70, 80], 65 不在列表中 未找到")
    print(f"实际结果: {'找到' if tree.search(65) else '未找到'}")


if __name__ == "__main__":
    # 运行测试
    test_btree()
    test_bplustree()
    demonstrate_btree_search()
    demonstrate_bplustree_search()

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
