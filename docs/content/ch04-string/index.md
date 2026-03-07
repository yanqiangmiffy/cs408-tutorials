# 第4章 串

> **考研要点速记**：串是特殊的线性表，元素为字符；KMP算法是考研必考点，核心是next数组的构造，时间复杂度O(m+n)。

## 1. 朴素模式匹配 <a id="naive"></a>

朴素模式匹配（BF算法）的基本思想是从主串的每一个位置开始，依次与子串比较，直到匹配成功或遍历完主串。

**时间复杂度**：最坏情况下O(m×n)，其中m为模式串长度，n为主串长度。

```python
def naive_match(text: str, pattern: str) -> int:
    """
    朴素模式匹配
    返回pattern在text中的起始位置，未找到返回-1
    """
    n, m = len(text), len(pattern)

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i  # 匹配成功

    return -1  # 匹配失败


# 测试
if __name__ == "__main__":
    text = "ABABCABCABABCD"
    pattern = "ABCAB"
    pos = naive_match(text, pattern)
    print(f"匹配位置: {pos}")  # 输出: 2
```

## 2. KMP算法 <a id="kmp"></a>

KMP算法利用已经部分匹配的有效信息，保持主串指针不回溯，通过修改模式串指针，让模式串尽量地移动到有效的位置。

### 核心思想

- `next[j]`：当模式串第j个字符匹配失败时，模式串指针应该回退到的位置
- `next[j]`的值等于模式串中`pattern[0:j]`的最长相等前后缀长度

### 手工计算next数组的方法

1. 写出模式串的所有前缀
2. 对每个前缀，找最长相等的前缀和后缀（不包括自身）
3. next[j]的值就是最长相等前后缀长度

**示例**：模式串 "ABABC"

| j | pattern[0:j] | 最长相等前后缀 | next[j] |
|---|--------------|----------------|---------|
| 0 | "" | - | -1 |
| 1 | "A" | 无 | 0 |
| 2 | "AB" | 无 | 0 |
| 3 | "ABA" | "A" | 1 |
| 4 | "ABAB" | "AB" | 2 |
| 5 | "ABABC" | 无 | 0 |

### Python实现

```python
def compute_next(pattern: str) -> list:
    """
    计算next数组
    next[j]表示当pattern[j]匹配失败时，应该回退到的位置
    """
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
    """
    KMP模式匹配
    返回pattern在text中的起始位置，未找到返回-1
    """
    if not pattern:
        return 0

    n, m = len(text), len(pattern)
    next_arr = compute_next(pattern)

    i, j = 0, 0  # i指向text，j指向pattern

    while i < n and j < m:
        if j == -1 or text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            j = next_arr[j]  # j回退到next[j]位置

    if j == m:
        return i - j
    return -1


# 测试
if __name__ == "__main__":
    text = "ABABCABCABABCD"
    pattern = "ABCAB"

    print(f"next数组: {compute_next(pattern)}")
    pos = kmp_match(text, pattern)
    print(f"匹配位置: {pos}")  # 输出: 2
```

## 考研重点 & 易错点

- ⚠️ 易错点：next数组的定义有多种版本，有的next[0]=-1，有的next[0]=0，考研时要注意题目要求
- 📌 高频考点：手工计算next数组，必须熟练掌握
- ⚠️ 易错点：KMP匹配过程中i不回溯，只有j回溯，这是KMP的核心优化
- 📌 高频考点：KMP算法的时间复杂度O(m+n)，朴素算法O(m×n)

## 复杂度总结表

| 算法 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 朴素匹配 | O(m×n) | O(1) |
| KMP预处理 | O(m) | O(m) |
| KMP匹配 | O(n) | O(m) |
| KMP总计 | O(m+n) | O(m) |
