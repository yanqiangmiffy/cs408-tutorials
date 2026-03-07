"""
线索二叉树 (Threaded Binary Tree)

核心思想: 利用二叉树中 n+1 个空指针域, 存放前驱/后继信息
  - ltag=0: left 指向左孩子; ltag=1: left 指向前驱
  - rtag=0: right 指向右孩子; rtag=1: right 指向后继

线索化类型:
  - 中序线索二叉树 (最常考)
  - 先序线索二叉树
  - 后序线索二叉树

考研要点:
  - 线索化的过程
  - 在线索二叉树中找前驱/后继
  - 空指针域公式: n个节点的二叉树有 n+1 个空指针域
"""


class ThreadedNode:
    """线索二叉树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.ltag = 0  # 0=左孩子, 1=前驱线索
        self.rtag = 0  # 0=右孩子, 1=后继线索

    def __repr__(self):
        return f"ThreadedNode({self.val})"


class InorderThreadedTree:
    """中序线索二叉树"""

    def __init__(self, root=None):
        self.root = root
        self.pre = None  # 线索化时记录前驱

    def create_thread(self):
        """中序线索化"""
        self.pre = None
        self._thread(self.root)
        # 处理最后一个节点的后继
        if self.pre and self.pre.right is None:
            self.pre.rtag = 1

    def _thread(self, node):
        """递归中序线索化

        思路: 按中序遍历, 遍历到每个节点时:
        1. 如果当前节点左孩子为空 → 左指针指向前驱 (pre)
        2. 如果前驱的右孩子为空 → 前驱的右指针指向当前节点 (后继)
        3. 更新 pre = 当前节点
        """
        if node is None:
            return

        # 左子树线索化
        self._thread(node.left)

        # 处理当前节点
        if node.left is None:     # 左孩子为空 → 建前驱线索
            node.left = self.pre
            node.ltag = 1

        if self.pre and self.pre.right is None:  # 前驱右孩子为空 → 建后继线索
            self.pre.right = node
            self.pre.rtag = 1

        self.pre = node

        # 右子树线索化
        self._thread(node.right)

    def inorder_first(self, node):
        """找以 node 为根的子树中, 中序遍历的第一个节点

        即: 一路向左走到底
        """
        while node and node.ltag == 0:
            node = node.left
        return node

    def inorder_next(self, node):
        """找 node 的中序后继

        两种情况:
        1. rtag == 1: 后继线索直接指向后继
        2. rtag == 0: 右子树中序遍历的第一个节点
        """
        if node.rtag == 1:
            return node.right
        return self.inorder_first(node.right)

    def inorder_last(self, node):
        """找以 node 为根的子树中, 中序遍历的最后一个节点"""
        while node and node.rtag == 0:
            node = node.right
        return node

    def inorder_prev(self, node):
        """找 node 的中序前驱

        两种情况:
        1. ltag == 1: 前驱线索直接指向前驱
        2. ltag == 0: 左子树中序遍历的最后一个节点
        """
        if node.ltag == 1:
            return node.left
        return self.inorder_last(node.left)

    def inorder_traverse(self):
        """利用线索进行中序遍历 (无需栈和递归!)"""
        result = []
        node = self.inorder_first(self.root)
        while node:
            result.append(node.val)
            node = self.inorder_next(node)
        return result

    def inorder_traverse_reverse(self):
        """逆向中序遍历"""
        result = []
        node = self.inorder_last(self.root)
        while node:
            result.append(node.val)
            node = self.inorder_prev(node)
        return result


def build_sample_tree():
    """构建示例二叉树
           A
          / \
         B   C
        / \   \
       D   E   F
    """
    a = ThreadedNode('A')
    b = ThreadedNode('B')
    c = ThreadedNode('C')
    d = ThreadedNode('D')
    e = ThreadedNode('E')
    f = ThreadedNode('F')
    a.left, a.right = b, c
    b.left, b.right = d, e
    c.right = f
    return a


def threading_demo():
    """线索化演示"""
    print("=" * 60)
    print("中序线索二叉树")
    print("=" * 60)

    root = build_sample_tree()
    tree = InorderThreadedTree(root)
    tree.create_thread()

    print(f"""
  原始二叉树:
         A
        / \\
       B   C
      / \\   \\
     D   E   F

  中序序列: D B E A C F
    """)

    # 展示线索
    print(f"  --- 线索化结果 ---")
    nodes = {'A': root, 'B': root.left, 'C': root.right,
             'D': root.left.left, 'E': root.left.right,
             'F': root.right.right}

    print(f"  {'节点':>4s} {'ltag':>4s} {'left':>6s} {'rtag':>4s} {'right':>6s}")
    print(f"  {'─' * 30}")
    for name, node in nodes.items():
        lt = "前驱" if node.ltag == 1 else "孩子"
        rt = "后继" if node.rtag == 1 else "孩子"
        l = node.left.val if node.left else "NULL"
        r = node.right.val if node.right else "NULL"
        print(f"  {name:>4s} {lt:>4s} {l:>6s} {rt:>4s} {r:>6s}")

    # 遍历
    print(f"\n  --- 利用线索遍历 ---")
    print(f"  正向中序: {tree.inorder_traverse()}")
    print(f"  逆向中序: {tree.inorder_traverse_reverse()}")

    # 找前驱后继
    print(f"\n  --- 找前驱后继 ---")
    for name, node in nodes.items():
        prev_node = tree.inorder_prev(node)
        next_node = tree.inorder_next(node)
        prev_val = prev_node.val if prev_node else "无"
        next_val = next_node.val if next_node else "无"
        print(f"  {name}: 前驱={prev_val}, 后继={next_val}")

    print()


if __name__ == "__main__":
    threading_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 空指针域: n 个节点有 2n 个指针域, 非空 n-1 个
     空指针域 = 2n - (n-1) = n + 1

  2. 线索化规则:
     左孩子为空 → ltag=1, left 指向前驱
     右孩子为空 → rtag=1, right 指向后继

  3. 找中序后继:
     rtag=1 → right 就是后继
     rtag=0 → 右子树中一路向左到底

  4. 找中序前驱:
     ltag=1 → left 就是前驱
     ltag=0 → 左子树中一路向右到底

  5. 优势: 遍历不需要栈和递归, O(1) 额外空间!
    """)
