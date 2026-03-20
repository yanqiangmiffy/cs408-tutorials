"""
哈夫曼树 (Huffman Tree) 与哈夫曼编码

核心概念:
  - 带权路径长度 WPL = Σ(wi × li)  (权值×路径长度)
  - 哈夫曼树: WPL 最小的二叉树
  - 哈夫曼编码: 前缀编码, 用于数据压缩

构造算法:
  1. 将所有节点作为独立的树放入集合
  2. 每次取权值最小的两棵树合并
  3. 合并后的树权值 = 两棵树权值之和
  4. 重复直到只剩一棵树

考研要点:
  - 手画哈夫曼树
  - 计算 WPL
  - 哈夫曼编码不唯一, 但 WPL 唯一
  - n 个叶子的哈夫曼树有 2n-1 个节点
"""

import heapq


class HuffmanNode:
    def __init__(self, char=None, weight=0):
        self.char = char
        self.weight = weight
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return f"HNode({self.char}:{self.weight})"


def build_huffman_tree(char_weights):
    """构造哈夫曼树

    char_weights: [(字符, 权值), ...]
    """
    # 创建叶子节点, 放入最小堆
    heap = []
    for char, weight in char_weights:
        node = HuffmanNode(char, weight)
        heapq.heappush(heap, node)

    print(f"  构造过程:")
    step = 0
    while len(heap) > 1:
        step += 1
        # 取两个最小的
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        # 合并
        parent = HuffmanNode(weight=left.weight + right.weight)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

        l_name = left.char if left.char else f"({left.weight})"
        r_name = right.char if right.char else f"({right.weight})"
        print(f"  步骤{step}: 合并 {l_name}({left.weight}) + "
              f"{r_name}({right.weight}) = {parent.weight}")

    return heap[0]


def get_huffman_codes(root):
    """获取哈夫曼编码

    左分支 = 0, 右分支 = 1
    """
    codes = {}

    def dfs(node, code):
        if node is None:
            return
        if node.char:  # 叶子节点
            codes[node.char] = code if code else '0'
            return
        dfs(node.left, code + '0')
        dfs(node.right, code + '1')

    dfs(root, '')
    return codes


def calculate_wpl(root, depth=0):
    """计算带权路径长度 WPL"""
    if root is None:
        return 0
    if root.char:  # 叶子节点
        return root.weight * depth
    return (calculate_wpl(root.left, depth + 1) +
            calculate_wpl(root.right, depth + 1))


def huffman_demo():
    """哈夫曼树构造和编码演示"""
    print("=" * 60)
    print("哈夫曼树构造")
    print("=" * 60)

    # 示例: 字符频率
    char_weights = [
        ('A', 5), ('B', 9), ('C', 12),
        ('D', 13), ('E', 16), ('F', 45)
    ]
    print(f"\n  字符权值: {char_weights}")
    print()

    root = build_huffman_tree(char_weights)

    # 计算 WPL
    wpl = calculate_wpl(root)
    print(f"\n  WPL = {wpl}")

    # 获取编码
    codes = get_huffman_codes(root)
    print(f"\n  哈夫曼编码:")
    total_bits = 0
    for char, weight in sorted(char_weights, key=lambda x: x[1]):
        code = codes[char]
        bits = weight * len(code)
        total_bits += bits
        print(f"  {char}: {code:>10s}  (权值={weight}, 编码长={len(code)}, w×l={bits})")
    print(f"  WPL = {total_bits}")

    # 编码示例
    print(f"\n  --- 编码/解码示例 ---")
    message = "ABCDEF"
    encoded = ''.join(codes[c] for c in message)
    print(f"  原文: {message}")
    print(f"  编码: {encoded}")
    print(f"  编码长度: {len(encoded)} bits")
    print(f"  等长编码需: {len(message) * 3} bits (3位/字符)")
    print(f"  压缩率: {len(encoded) / (len(message) * 3) * 100:.1f}%")
    print()


def wpl_comparison():
    """WPL 对比: 哈夫曼 vs 其他方案"""
    print("=" * 60)
    print("WPL 对比")
    print("=" * 60)

    weights = [7, 5, 2, 4]
    print(f"\n  权值: {weights}")

    print(f"""
  方案1 (完全二叉树):       方案2 (哈夫曼树):
        (18)                    (18)
       /    \\                  /    \\
     (12)    (6)             (11)   (7)
    /   \\   /  \\            /   \\
   7    5  2    4          (6)    5
                          /   \\
                         2     4

  WPL1 = 7×2+5×2+2×2+4×2 = 36
  WPL2 = 7×1+5×2+2×3+4×3 = 35
    """)

    # 用算法验证
    char_weights = [('a', 7), ('b', 5), ('c', 2), ('d', 4)]
    root = build_huffman_tree(char_weights)
    wpl = calculate_wpl(root)
    print(f"  哈夫曼树 WPL = {wpl} (最优!)")
    print()


if __name__ == "__main__":
    huffman_demo()
    wpl_comparison()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 哈夫曼树性质:
     - n 个叶子节点 → 共 2n-1 个节点
     - 没有度为 1 的节点
     - WPL 最小 (最优二叉树)

  2. 构造算法:
     每次取最小两个合并，重复 n-1 次

  3. 哈夫曼编码:
     - 是前缀编码 (任一字符编码都不是另一个的前缀)
     - 编码不唯一 (左右孩子可交换), 但 WPL 唯一
     - 权值大的编码短, 权值小的编码长

  4. WPL = Σ(wi × li)
     wi: 叶子权值, li: 叶子到根的路径长度
    """)
