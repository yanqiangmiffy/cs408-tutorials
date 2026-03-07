"""
二叉树的遍历 (Binary Tree Traversal)

四种遍历方式:
  1. 先序遍历 (Pre-order):  根 → 左 → 右
  2. 中序遍历 (In-order):   左 → 根 → 右
  3. 后序遍历 (Post-order):  左 → 右 → 根
  4. 层次遍历 (Level-order): 逐层从左到右 (用队列)

考研要点:
  - 递归和非递归实现
  - 由遍历序列构造二叉树 (中序 + 先/后/层序)
  - 遍历序列的手写推导
"""

from collections import deque


class TreeNode:
    """二叉树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.val})"


def build_sample_tree():
    """构建示例二叉树
           A
          / \
         B   C
        / \   \
       D   E   F
    """
    root = TreeNode('A')
    root.left = TreeNode('B')
    root.right = TreeNode('C')
    root.left.left = TreeNode('D')
    root.left.right = TreeNode('E')
    root.right.right = TreeNode('F')
    return root


# ==========================================
# 递归遍历
# ==========================================

def preorder(root):
    """先序遍历 (递归): 根左右"""
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


def inorder(root):
    """中序遍历 (递归): 左根右"""
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def postorder(root):
    """后序遍历 (递归): 左右根"""
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# ==========================================
# 非递归遍历 (用栈)
# ==========================================

def preorder_iterative(root):
    """先序遍历 (非递归)

    思路: 栈中根节点先出, 右孩子先入栈(后出), 左孩子后入栈(先出)
    """
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:  # 右孩子先入栈
            stack.append(node.right)
        if node.left:   # 左孩子后入栈
            stack.append(node.left)
    return result


def inorder_iterative(root):
    """中序遍历 (非递归)

    思路: 一路向左到底, 然后弹出, 转向右子树
    """
    result = []
    stack = []
    cur = root
    while cur or stack:
        while cur:  # 一路向左
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right  # 转向右子树
    return result


def postorder_iterative(root):
    """后序遍历 (非递归)

    思路: 先序是 根左右, 改为 根右左, 再反转得 左右根 (后序)
    """
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:   # 左先入栈
            stack.append(node.left)
        if node.right:  # 右后入栈
            stack.append(node.right)
    return result[::-1]  # 反转


# ==========================================
# 层次遍历 (BFS)
# ==========================================

def level_order(root):
    """层次遍历 (用队列)"""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


def level_order_by_level(root):
    """分层输出的层次遍历"""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# ==========================================
# 由遍历序列构造二叉树
# ==========================================

def build_from_preorder_inorder(preorder_seq, inorder_seq):
    """由先序+中序构造二叉树

    思路:
    1. 先序的第一个元素是根
    2. 在中序中找到根, 左边是左子树, 右边是右子树
    3. 递归构建
    """
    if not preorder_seq or not inorder_seq:
        return None
    root_val = preorder_seq[0]
    root = TreeNode(root_val)
    idx = inorder_seq.index(root_val)

    root.left = build_from_preorder_inorder(
        preorder_seq[1:1 + idx], inorder_seq[:idx])
    root.right = build_from_preorder_inorder(
        preorder_seq[1 + idx:], inorder_seq[idx + 1:])
    return root


def build_from_postorder_inorder(postorder_seq, inorder_seq):
    """由后序+中序构造二叉树

    思路: 后序的最后一个元素是根
    """
    if not postorder_seq or not inorder_seq:
        return None
    root_val = postorder_seq[-1]
    root = TreeNode(root_val)
    idx = inorder_seq.index(root_val)

    root.left = build_from_postorder_inorder(
        postorder_seq[:idx], inorder_seq[:idx])
    root.right = build_from_postorder_inorder(
        postorder_seq[idx:-1], inorder_seq[idx + 1:])
    return root


def print_tree(root, prefix="", is_left=True):
    """可视化打印二叉树"""
    if root is None:
        return
    print(f"  {prefix}{'├── ' if is_left else '└── '}{root.val}")
    if root.left or root.right:
        if root.left:
            print_tree(root.left, prefix + ("│   " if not is_left else "    "), True)
        if root.right:
            print_tree(root.right, prefix + ("│   " if not is_left else "    "), False)


def traversal_demo():
    """遍历演示"""
    print("=" * 60)
    print("二叉树的四种遍历")
    print("=" * 60)

    root = build_sample_tree()
    print(f"\n  二叉树结构:")
    print(f"         A")
    print(f"        / \\")
    print(f"       B   C")
    print(f"      / \\   \\")
    print(f"     D   E   F")

    print(f"\n  先序 (根左右): {preorder(root)}")
    print(f"  中序 (左根右): {inorder(root)}")
    print(f"  后序 (左右根): {postorder(root)}")
    print(f"  层序:          {level_order(root)}")

    print(f"\n  --- 非递归实现 ---")
    print(f"  先序 (非递归): {preorder_iterative(root)}")
    print(f"  中序 (非递归): {inorder_iterative(root)}")
    print(f"  后序 (非递归): {postorder_iterative(root)}")

    print(f"\n  分层输出: {level_order_by_level(root)}")
    print()


def build_tree_demo():
    """由遍历序列构造二叉树"""
    print("=" * 60)
    print("由遍历序列构造二叉树")
    print("=" * 60)

    pre = ['A', 'B', 'D', 'E', 'C', 'F']
    ino = ['D', 'B', 'E', 'A', 'C', 'F']
    post = ['D', 'E', 'B', 'F', 'C', 'A']

    print(f"\n  先序: {pre}")
    print(f"  中序: {ino}")
    print(f"  后序: {post}")

    # 先序+中序
    print(f"\n  --- 先序 + 中序 → 构造二叉树 ---")
    root1 = build_from_preorder_inorder(pre, ino)
    print(f"  验证先序: {preorder(root1)}")
    print(f"  验证中序: {inorder(root1)}")
    print(f"  验证后序: {postorder(root1)}")

    # 后序+中序
    print(f"\n  --- 后序 + 中序 → 构造二叉树 ---")
    root2 = build_from_postorder_inorder(post, ino)
    print(f"  验证先序: {preorder(root2)}")
    print(f"  验证后序: {postorder(root2)}")

    print(f"""
  ⚠️ 注意:
  - 中序序列是必须的! (先序+后序不能唯一确定)
  - 先序+中序 → 唯一确定
  - 后序+中序 → 唯一确定
  - 层序+中序 → 唯一确定
    """)


def tree_properties():
    """二叉树性质"""
    print("=" * 60)
    print("二叉树的重要性质")
    print("=" * 60)
    print("""
  1. 第 i 层最多有 2^(i-1) 个节点 (i >= 1)
  2. 深度为 k 的二叉树最多有 2^k - 1 个节点
  3. n0 = n2 + 1 (叶子数 = 度为2的节点数 + 1)
  4. 完全二叉树:
     - n 个节点的深度 = ⌊log₂n⌋ + 1
     - 节点 i 的父节点: ⌊i/2⌋
     - 节点 i 的左孩子: 2i
     - 节点 i 的右孩子: 2i + 1
  5. 满二叉树: 每层都满, 共 2^k - 1 个节点
    """)


if __name__ == "__main__":
    traversal_demo()
    build_tree_demo()
    tree_properties()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 遍历助记:
     先序: 根左右 (NLR)
     中序: 左根右 (LNR)
     后序: 左右根 (LRN)

  2. 非递归中序:
     一路向左到底 → 弹出访问 → 转向右子树

  3. 非递归后序:
     改造先序为 根右左 → 反转得到 左右根

  4. 由序列构造:
     必须有中序! 先序/后序/层序 + 中序 → 唯一确定

  5. n0 = n2 + 1 (最常考的性质!)
    """)
