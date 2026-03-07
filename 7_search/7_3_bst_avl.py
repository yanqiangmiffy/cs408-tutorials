"""
二叉排序树 (BST) 和 平衡二叉树 (AVL)

1. BST (Binary Search Tree):
   - 左子树所有节点 < 根 < 右子树所有节点
   - 中序遍历得到有序序列
   - 查找/插入/删除 平均 O(log n), 最坏 O(n)

2. AVL (平衡二叉树):
   - BST + |左右子树高度差| <= 1
   - 通过旋转保持平衡
   - 查找/插入/删除 O(log n) (最坏也是)

考研要点:
  - BST 的查找、插入、删除操作
  - AVL 的四种旋转 (LL, RR, LR, RL)
  - AVL 插入后的调整
"""


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# ==========================================
# BST 操作
# ==========================================

def bst_insert(root, key):
    """BST 插入"""
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    elif key > root.key:
        root.right = bst_insert(root.right, key)
    return root


def bst_search(root, key):
    """BST 查找"""
    if root is None or root.key == key:
        return root
    if key < root.key:
        return bst_search(root.left, key)
    return bst_search(root.right, key)


def bst_delete(root, key):
    """BST 删除

    三种情况:
    1. 叶子节点: 直接删除
    2. 只有一个孩子: 用孩子替代
    3. 有两个孩子: 用中序后继(右子树最小值)替代, 再删后继
    """
    if root is None:
        return None
    if key < root.key:
        root.left = bst_delete(root.left, key)
    elif key > root.key:
        root.right = bst_delete(root.right, key)
    else:  # 找到了
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        else:
            # 找中序后继 (右子树最小值)
            successor = root.right
            while successor.left:
                successor = successor.left
            root.key = successor.key
            root.right = bst_delete(root.right, successor.key)
    return root


def bst_inorder(root):
    if root is None:
        return []
    return bst_inorder(root.left) + [root.key] + bst_inorder(root.right)


# ==========================================
# AVL 树
# ==========================================

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def height(node):
    return node.height if node else 0


def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0


def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1


def rotate_right(y):
    """右旋 (LL 型)

    适用: 在左子树的左孩子插入导致不平衡

        y              x
       / \           /   \
      x   T3   →   T1     y
     / \                  / \
    T1  T2              T2   T3
    """
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    update_height(y)
    update_height(x)
    return x


def rotate_left(x):
    """左旋 (RR 型)

    适用: 在右子树的右孩子插入导致不平衡

      x                y
     / \             /   \
    T1   y    →    x      T3
        / \       / \
       T2  T3   T1   T2
    """
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y


def avl_insert(root, key):
    """AVL 插入 + 自动平衡

    四种不平衡:
    LL: bf > 1 且 key < root.left.key → 右旋
    RR: bf < -1 且 key > root.right.key → 左旋
    LR: bf > 1 且 key > root.left.key → 先左旋左子树, 再右旋
    RL: bf < -1 且 key < root.right.key → 先右旋右子树, 再左旋
    """
    if root is None:
        return AVLNode(key)
    if key < root.key:
        root.left = avl_insert(root.left, key)
    elif key > root.key:
        root.right = avl_insert(root.right, key)
    else:
        return root

    update_height(root)
    bf = balance_factor(root)

    # LL
    if bf > 1 and key < root.left.key:
        return rotate_right(root)
    # RR
    if bf < -1 and key > root.right.key:
        return rotate_left(root)
    # LR
    if bf > 1 and key > root.left.key:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    # RL
    if bf < -1 and key < root.right.key:
        root.right = rotate_right(root.right)
        return rotate_left(root)

    return root


def avl_inorder(root):
    if root is None:
        return []
    return avl_inorder(root.left) + [root.key] + avl_inorder(root.right)


def print_tree(root, prefix="", is_left=True):
    """可视化打印"""
    if root is None:
        return
    print(f"  {prefix}{'├── ' if is_left else '└── '}{root.key}", end="")
    if hasattr(root, 'height'):
        print(f" (h={root.height}, bf={balance_factor(root)})")
    else:
        print()
    new_prefix = prefix + ("│   " if is_left else "    ")
    if root.left or root.right:
        if root.left:
            print_tree(root.left, new_prefix, True)
        else:
            print(f"  {new_prefix}├── (空)")
        if root.right:
            print_tree(root.right, new_prefix, False)
        else:
            print(f"  {new_prefix}└── (空)")


def bst_demo():
    """BST 演示"""
    print("=" * 60)
    print("二叉排序树 (BST)")
    print("=" * 60)

    keys = [50, 30, 70, 20, 40, 60, 80]
    root = None
    for k in keys:
        root = bst_insert(root, k)
    print(f"\n  插入序列: {keys}")
    print(f"  中序遍历: {bst_inorder(root)}")
    print(f"  树结构:")
    print_tree(root)

    # 查找
    print(f"\n  查找 40: {'找到' if bst_search(root, 40) else '未找到'}")
    print(f"  查找 45: {'找到' if bst_search(root, 45) else '未找到'}")

    # 删除
    print(f"\n  删除 50 (有两个孩子):")
    root = bst_delete(root, 50)
    print(f"  中序遍历: {bst_inorder(root)}")
    print_tree(root)
    print()


def avl_demo():
    """AVL 演示"""
    print("=" * 60)
    print("平衡二叉树 (AVL)")
    print("=" * 60)

    root = None
    keys = [50, 30, 70, 20, 40, 10]  # 插入 10 时触发 LL 旋转

    for i, k in enumerate(keys):
        root = avl_insert(root, k)
        print(f"\n  插入 {k}:")
        print_tree(root)

    print(f"\n  中序遍历: {avl_inorder(root)}")

    # 演示各种旋转
    print(f"""
  四种旋转:
  ┌─────┬─────────────────────────────────────────┐
  │ LL  │ 左子树的左孩子插入 → 右旋              │
  │ RR  │ 右子树的右孩子插入 → 左旋              │
  │ LR  │ 左子树的右孩子插入 → 先左旋再右旋      │
  │ RL  │ 右子树的左孩子插入 → 先右旋再左旋      │
  └─────┴─────────────────────────────────────────┘
    """)


if __name__ == "__main__":
    bst_demo()
    avl_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. BST 性质:
     左 < 根 < 右
     中序遍历 = 有序序列
     ASL 取决于树的形状 (最坏退化为链表)

  2. BST 删除:
     叶子: 直接删
     一个孩子: 子承父业
     两个孩子: 用中序后继/前驱替代

  3. AVL 四种旋转:
     LL: 右旋
     RR: 左旋
     LR: 先左旋后右旋
     RL: 先右旋后左旋

  4. AVL 高度 h 的最少节点:
     n(h) = n(h-1) + n(h-2) + 1
     类似斐波那契数列
    """)
