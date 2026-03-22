# 第4章 串

> 串是特殊的线性表，每个数据元素是一个字符。字符串匹配是计算机科学中的经典问题，朴素匹配简单但效率低，KMP算法通过预处理模式串实现高效匹配。

---

## 0. 串的定义与特性

| 概念 | 定义 / 特性 |
|------|-------------|
| **串（String）** | 由零个或多个字符组成的有限序列，通常记为 `S = "a₁a₂...aₙ"` |
| **串长** | 串中字符个数；长度为 0 的串称为空串 `""` |
| **空格串** | 由一个或多个空格组成，不是空串，长度大于 0 |
| **主串 / 模式串** | 待查找的串称主串，被拿来匹配的串称模式串 |
| **子串** | 串中任意连续字符组成的序列；不连续字符不能构成子串 |
| **位置敏感** | 串中字符相同但顺序不同，通常视为不同的串 |

**考试里最常问的几个点**：

- 空串和空格串一定要区分。
- 子串必须连续，子序列可以不连续。
- 串是特殊的线性表，比较时通常按字符逐个进行。
- 模式匹配题里，主串长度记为 `n`，模式串长度记为 `m`，复杂度通常写成 `O(n)`、`O(m)`、`O(nm)`、`O(n+m)`。

## 1. 朴素模式匹配（BF算法）<a id="naive"></a>

**核心思想**：从主串的每个位置开始，依次与模式串比较。匹配失败时，主串指针向后移一位，模式串指针重置为0，重新开始比较。

**时间复杂度**：
- 最好：O(n)（模式串在主串开头就匹配）
- 最坏：O(m×n)（每个位置都要比较到模式串末尾才失败）

### 匹配过程（手写示例）

**主串**: `"ABABABC"` (n=7)  
**模式串**: `"ABABC"` (m=5)

```
第1轮 i=0:
  主串:  A B A B A B C
  模式:  A B A B C
  比较:  A==A, B==B, A==A, B==B, A!=C ✗ 失败！

第2轮 i=1:
  主串:  A B A B A B C
  模式:    A B A B C
  比较:  B!=A ✗ 失败！

第3轮 i=2:
  主串:  A B A B A B C
  模式:      A B A B C
  比较:  A==A, B==B, A==A, B==B, C==C ✓ 匹配成功！

返回: 2
```

### Python实现

```python
def naive_match(text: str, pattern: str) -> int:
    """
    朴素模式匹配（BF算法）
    返回pattern在text中的起始位置，未找到返回-1

    时间复杂度: O(m×n), m为模式串长度，n为主串长度
    空间复杂度: O(1)
    """
    n, m = len(text), len(pattern)

    # 遍历主串的所有可能起始位置
    for i in range(n - m + 1):
        j = 0  # 模式串指针

        # 依次比较字符
        while j < m and text[i + j] == pattern[j]:
            j += 1

        # j==m 表示模式串全部匹配成功
        if j == m:
            return i

    return -1  # 未找到
```

---

## 2. KMP算法 <a id="kmp"></a>

**核心思想**：利用已经部分匹配的有效信息，主串指针不回溯，通过修改模式串指针，让模式串尽量移动到有效位置。

**关键优化**：当匹配失败时，主串指针i不回溯，模式串指针j回退到next[j]位置，而不是回退到0。

### 为什么 KMP 能做到“主串不回退”

这里最容易卡住。直觉上可以这样想：

- 当 `pattern[0:j]` 已经和主串某一段匹配成功时，这段信息其实已经花时间验证过了。
- 一旦在 `pattern[j]` 失配，没必要让主串回到旧位置重比，因为主串那一段字符我们已经看过。
- 真正需要调整的是模式串：把它往右滑到“前面已经匹配成功的部分里，仍然可能继续匹配”的位置。
- `next[j]` 记录的就是这个“还能接着试”的最远合法落点。

所以 KMP 省下来的，不是比较本身，而是避免了大量“明知会失败的重复回头路”。

### next数组含义

`next[j]` 表示：当模式串第j个字符匹配失败时，模式串指针应该回退到的位置。

**数学定义**：`next[j]` 等于模式串 `pattern[0:j]` 的**最长相等前后缀**长度（不包括自身）。

**前缀和后缀**：
- 前缀：从开头到某位置（不包括整个串）
- 后缀：从某位置到结尾（不包括整个串）

> 说明：教材里常见两种记法。  
> 1. **手算版扩展 next**：长度为 `m+1`，便于推演匹配过程。  
> 2. **代码版 next**：长度为 `m`，更常见于程序实现。  
> 本文两种都会给出，避免概念和代码对不上。

### 手工计算next数组

**模式串**: `"ABABC"`

| j | pattern[0:j] | 前缀 | 后缀 | 最长相等前后缀 | next[j] |
|---|--------------|------|------|----------------|---------|
| 0 | `""` | - | - | - | -1 |
| 1 | `"A"` | - | - | 无 | 0 |
| 2 | `"AB"` | `"A"` | `"B"` | 无 | 0 |
| 3 | `"ABA"` | `"A"`, `"AB"` | `"BA"`, `"A"` | `"A"` | 1 |
| 4 | `"ABAB"` | `"A"`, `"AB"`, `"ABA"` | `"BAB"`, `"AB"`, `"B"` | `"AB"` | 2 |
| 5 | `"ABABC"` | `"A"`, `"AB"`, `"ABA"`, `"ABAB"` | `"BABC"`, `"ABC"`, `"BC"`, `"C"` | 无 | 0 |

**手算版扩展 next**: `[-1, 0, 0, 1, 2, 0]`  
**代码版 next**: `[-1, 0, 0, 1, 2]`

### next数组计算过程

**模式串**: `"ABABC"`

```
j=0, k=-1:  next[0] = -1

j=0, k=-1:  k==-1，令 j=1, k=0
            next[1] = 0

j=1, k=0:   pattern[1]='B' != pattern[0]='A'
            k = next[0] = -1
j=1, k=-1:  k==-1，令 j=2, k=0
            next[2] = 0

j=2, k=0:   pattern[2]='A' == pattern[0]='A'
            令 j=3, k=1
            next[3] = 1

j=3, k=1:   pattern[3]='B' == pattern[1]='B'
            令 j=4, k=2
            next[4] = 2

j=4, k=2:   pattern[4]='C' != pattern[2]='A'
            k = next[2] = 0
j=4, k=0:   pattern[4]='C' != pattern[0]='A'
            k = next[0] = -1
j=4, k=-1:  k==-1，令 j=5, k=0
            next[5] = 0

结果:
扩展 next = [-1, 0, 0, 1, 2, 0]
代码版 next = [-1, 0, 0, 1, 2]
```

### KMP匹配过程（手写示例）

**主串**: `"ABABABC"`  
**模式串**: `"ABABC"`  
**代码版 next数组**: `[-1, 0, 0, 1, 2]`

```
初始 i=0, j=0:
  主串:  A B A B A B C
  模式:  A B A B C
  i=0, j=0: A==A, i++, j++

i=1, j=1:
  主串:  A B A B A B C
  模式:  A B A B C
  i=1, j=1: B==B, i++, j++

i=2, j=2:
  主串:  A B A B A B C
  模式:  A B A B C
  i=2, j=2: A==A, i++, j++

i=3, j=3:
  主串:  A B A B A B C
  模式:  A B A B C
  i=3, j=3: B==B, i++, j++

i=4, j=4:
  主串:  A B A B A B C
  模式:  A B A B C
  i=4, j=4: A!=C ✗ 失败！
  j = next[4] = 2，主串指针 i 不回退

i=4, j=2:
  主串:  A B A B A B C
  模式:      A B A B C
  i=4, j=2: A==A, i++, j++

i=5, j=3:
  主串:  A B A B A B C
  模式:      A B A B C
  i=5, j=3: B==B, i++, j++

i=6, j=4:
  主串:  A B A B A B C
  模式:      A B A B C
  i=6, j=4: C==C, i++, j++

j==5 (m) ✓ 匹配成功
返回 i-j = 7-5 = 2
```

### Python实现

```python
def compute_next(pattern: str) -> list:
    """
    计算next数组
    next[j]表示当pattern[j]匹配失败时，应该回退到的位置

    时间复杂度: O(m)
    空间复杂度: O(m)
    """
    m = len(pattern)
    next_arr = [-1] * m
    i, j = 0, -1  # i当前计算位置，j前缀匹配位置

    while i < m - 1:
        if j == -1 or pattern[i] == pattern[j]:
            # 匹配成功，i和j都前进
            i += 1
            j += 1
            next_arr[i] = j
        else:
            # 匹配失败，j回退到next[j]
            j = next_arr[j]

    return next_arr


def kmp_match(text: str, pattern: str) -> int:
    """
    KMP模式匹配
    返回pattern在text中的起始位置，未找到返回-1

    时间复杂度: O(m+n), m为模式串长度，n为主串长度
    空间复杂度: O(m) 存储next数组
    """
    if not pattern:
        return 0

    n, m = len(text), len(pattern)
    next_arr = compute_next(pattern)

    i, j = 0, 0  # i指向text，j指向pattern

    while i < n and j < m:
        if j == -1 or text[i] == pattern[j]:
            # 匹配成功或j==-1（重置），两个指针都前进
            i += 1
            j += 1
        else:
            # 匹配失败，主串指针i不回溯，模式串j回退
            j = next_arr[j]

    # j==m 表示模式串全部匹配
    if j == m:
        return i - j
    return -1


if __name__ == "__main__":
    text = "ABABABC"
    pattern = "ABABC"

    print(f"主串: {text}")
    print(f"模式串: {pattern}")
    print(f"next数组: {compute_next(pattern)}")
    print(f"匹配位置: {kmp_match(text, pattern)}")
```

---

## 3. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **next数组计算** | 最长相等前后缀长度，必须手工计算 |
| **KMP vs 朴素** | KMP主串不回溯，时间复杂度O(m+n) |
| **next数组定义** | 有的版本next[0]=-1，有的next[0]=0 |
| **nextval数组** | nextval优化避免重复比较 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| next数组定义 | 注意题目要求的版本（-1或0开头） |
| KMP主串指针 | 匹配失败时i不回溯，只有j回退 |
| next数组计算 | 最长相等前后缀，不包括整个串本身 |
| 时间复杂度 | KMP是O(m+n)，朴素是O(m×n) |

### 手工计算技巧

1. 写出模式串的每个前缀
2. 对每个前缀，列出所有可能的前缀和后缀
3. 找最长相等的前缀和后缀
4. 长度即为next值

**快速计算示例**：`"ABAB"`

```
前缀"ABAB": 前缀={A,AB,ABA}, 后缀={BAB,AB,B}
最长相等前后缀: "AB" (长度2)
所以next[4] = 2
```

---

## 4. 复杂度对比表

| 算法 | 时间复杂度 | 空间复杂度 | 特点 |
|------|-----------|-----------|------|
| 朴素匹配 | O(m×n) | O(1) | 简单直观，效率低 |
| KMP预处理 | O(m) | O(m) | 预处理next数组 |
| KMP匹配 | O(n) | O(m) | 主串不回溯 |
| KMP总计 | O(m+n) | O(m) | 高效算法 |

---

## 5. next数组优化（nextval）

**核心思想**：当 `pattern[j] == pattern[next[j]]` 时，就算先回退到 `next[j]`，下一次往往还是会拿同一个字符去比较，属于重复失败。  
因此可以继续向前跳，直接使用更优的回退位置：

```text
若 pattern[j] == pattern[next[j]]
则 nextval[j] = nextval[next[j]]

若 pattern[j] != pattern[next[j]]
则 nextval[j] = next[j]
```

### 手算 nextval 的推荐顺序

1. 先算普通 `next` 数组。
2. 再从左到右计算 `nextval`。
3. 每一步只看两件事：`pattern[j]` 和 `pattern[next[j]]` 是否相等。
4. 相等就继续“沿着 nextval 往前跳”；不相等就直接取 `next[j]`。

### nextval 手算例子（详细）

**模式串**：`"AAAAB"`

先算普通 `next` 数组：

| j | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pattern[j] | A | A | A | A | B |
| next[j] | -1 | 0 | 1 | 2 | 3 |

接着从左到右计算 `nextval`：

- `j=0`：按定义，`nextval[0] = -1`
- `j=1`：`next[1] = 0`，比较 `pattern[1] = 'A'` 和 `pattern[0] = 'A'`
  两者相等，说明如果失配后只退到 0，主串当前字符还会再次和 `'A'` 比较，属于重复比较  
  所以 `nextval[1] = nextval[0] = -1`
- `j=2`：`next[2] = 1`，比较 `pattern[2] = 'A'` 和 `pattern[1] = 'A'`
  仍然相等，继续向前跳  
  所以 `nextval[2] = nextval[1] = -1`
- `j=3`：`next[3] = 2`，比较 `pattern[3] = 'A'` 和 `pattern[2] = 'A'`
  仍然相等，继续向前跳  
  所以 `nextval[3] = nextval[2] = -1`
- `j=4`：`next[4] = 3`，比较 `pattern[4] = 'B'` 和 `pattern[3] = 'A'`
  这次不相等，说明回退到 3 是有意义的，因为接下来比较的字符变了  
  所以 `nextval[4] = next[4] = 3`

整理成表：

| j | pattern[j] | next[j] | 比较对象 `pattern[next[j]]` | 是否相等 | nextval[j] |
|---|------------|---------|-----------------------------|----------|------------|
| 0 | A | -1 | - | - | -1 |
| 1 | A | 0 | A | 相等 | -1 |
| 2 | A | 1 | A | 相等 | -1 |
| 3 | A | 2 | A | 相等 | -1 |
| 4 | B | 3 | A | 不相等 | 3 |

**最终结果**：`nextval = [-1, -1, -1, -1, 3]`

### 为什么这个例子能体现优化

假设模式串已经匹配到 `j=3`，此时要拿主串当前字符去和 `pattern[3] = 'A'` 比较，但结果失配。

- 如果使用普通 `next`，会发生：`j = 3 -> 2 -> 1 -> 0 -> -1`
- 这意味着主串当前这个字符，会连续和多个 `'A'` 比较很多次
- 但这些比较其实没有意义，因为 `pattern[3]`、`pattern[2]`、`pattern[1]`、`pattern[0]` 都是 `'A'`

而使用 `nextval` 时：

- `j = 3 -> -1`
- 直接跳过这些“必然重复失败”的 `'A'`
- 所以 `nextval` 的本质，就是**跳过会导致重复比较的位置**

### 极简示例：模式串 `"AAA"`

| j | pattern[j] | next[j] | nextval[j] |
|---|------------|---------|------------|
| 0 | A | -1 | -1 |
| 1 | A | 0 | -1 (`A==A`，取 `nextval[0]`) |
| 2 | A | 1 | -1 (`A==A`，取 `nextval[1]`) |

**优势**：减少不必要的比较。

```python
def compute_nextval(pattern: str) -> list:
    """计算优化后的nextval数组"""
    m = len(pattern)
    if m == 0:
        return []

    next_arr = compute_next(pattern)
    nextval = [-1] * m

    for j in range(1, m):
        k = next_arr[j]
        if k != -1 and pattern[j] == pattern[k]:
            nextval[j] = nextval[k]
        else:
            nextval[j] = k

    return nextval
```

---

## 📝 完整代码示例

```python
def naive_match(text: str, pattern: str) -> int:
    """朴素模式匹配"""
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1


def compute_next(pattern: str) -> list:
    """计算next数组"""
    m = len(pattern)
    next_arr = [-1] * m
    i, j = 0, -1
    while i < m - 1:
        if j == -1 or pattern[i] == pattern[j]:
            i += 1
            j += 1
            next_arr[i] = j
        else:
            j = next_arr[j]
    return next_arr


def kmp_match(text: str, pattern: str) -> int:
    """KMP模式匹配"""
    if not pattern:
        return 0
    n, m = len(text), len(pattern)
    next_arr = compute_next(pattern)
    i, j = 0, 0
    while i < n and j < m:
        if j == -1 or text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            j = next_arr[j]
    return i - j if j == m else -1


if __name__ == "__main__":
    text = "ABABABC"
    pattern = "ABABC"

    print("=" * 40)
    print(f"主串: {text}")
    print(f"模式串: {pattern}")
    print("=" * 40)

    print("\n【朴素匹配】")
    pos_naive = naive_match(text, pattern)
    print(f"匹配位置: {pos_naive}")

    print("\n【KMP算法】")
    next_arr = compute_next(pattern)
    print(f"next数组: {next_arr}")
    pos_kmp = kmp_match(text, pattern)
    print(f"匹配位置: {pos_kmp}")

    print("\n【复杂度对比】")
    print(f"朴素匹配: O(m×n) = O({len(pattern)}×{len(text)}) = O({len(pattern) * len(text)})")
    print(f"KMP算法: O(m+n) = O({len(pattern)}+{len(text)}) = O({len(pattern) + len(text)})")
```

## 常考题型与相关算法题

### 常考点

- 串、子串、子序列、空串、空格串的区别。
- 朴素匹配为什么最坏是 `O(nm)`。
- `next` / `nextval` 的手工计算，尤其是最长相等前后缀的判断。
- KMP 失配时 **主串指针不回退**，只调整模式串指针。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| LeetCode 28. 找出字符串中第一个匹配项的下标 | 朴素匹配 / KMP 基础 |
| LeetCode 459. 重复的子字符串 | 前后缀、周期串 |
| LeetCode 796. 旋转字符串 | 串匹配思路 |
| LeetCode 1392. 最长快乐前缀 | `next` 数组本质 |
| LeetCode 214. 最短回文串 | KMP 前缀函数的综合应用 |
