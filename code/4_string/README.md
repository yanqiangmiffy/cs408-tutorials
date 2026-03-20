# 408考研 · 串（字符串）总结

> 本文档包含串的模式匹配算法的完整总结，涵盖朴素匹配(BF)和 KMP 算法的算法思想、next/nextval 数组手算方法、手写匹配过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 算法对比总览

| 算法 | 时间复杂度 | 主串回溯 | 核心思想 |
|------|-----------|---------|---------|
| 朴素匹配 (BF) | O(m×n) | ✅ 回溯 | 暴力逐位尝试 |
| KMP | O(m+n) | ❌ 不回溯 | 利用 next 数组跳转 |

> **n** = 主串长度，**m** = 模式串长度

---

## 1. 朴素模式匹配 (BF 算法)

**核心思想**：从主串的每个位置开始，逐个字符与模式串比较。匹配失败时，主串指针回溯到下一个起始位置，模式串指针回到开头。

**关键步骤**：
1. `i` 从 0 遍历主串每个可能的起始位置
2. 从 `i` 开始逐个字符与模式串比较
3. 全部匹配成功则返回 `i`
4. 有一个不匹配则 `i++`，重新开始

**手写匹配过程**（主串: `"aaaaab"`，模式串: `"aab"`）：

```
主串:   a a a a a b
模式串: a a b

第1次 i=0:  a a a a a b
            a a b
            ✓ ✓ ✗       arr[2]='a' ≠ 'b', 失败, i回溯到1

第2次 i=1:  a a a a a b
              a a b
              ✓ ✓ ✗     失败, i回溯到2

第3次 i=2:  a a a a a b
                a a b
                ✓ ✓ ✗   失败, i回溯到3

第4次 i=3:  a a a a a b
                  a a b
                  ✓ ✓ ✓ 匹配成功! 返回 i=3
```

> 每次失败 i 都回溯，浪费大量比较 → KMP 优化

**Python 实现**：

```python
def brute_force(text, pattern):
    """朴素模式匹配 O(m×n)"""
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i  # 匹配成功
    return -1
```

---

## 2. KMP 算法

**核心思想**：利用已匹配的信息，主串指针 `i` **永不回溯**，模式串指针 `j` 按 next 数组跳转到合适位置继续匹配。

### 2.1 next 数组

**含义**：`next[j]` = 模式串 `pattern[0..j-1]` 中**最长公共前后缀**的长度。匹配失败时 `j` 跳转到 `next[j]`。

**手算 next 数组**（模式串: `"abaabcac"`）：

```
j:       0    1    2    3    4    5    6    7
字符:    a    b    a    a    b    c    a    c
next:   -1    0    0    1    1    2    0    1

手算过程:
j=0: next[0] = -1  (约定)
j=1: next[1] = 0   (约定)
j=2: "a", 无公共前后缀 → 0
j=3: "ab", 无公共前后缀 → 0; 但 "aba" → 前缀"a"=后缀"a" → 1
j=3: "aba", "a"="a" → 1
j=4: "abaa", "a"与"a" → 1
j=5: "abaab", "ab"="ab" → 2
j=6: "abaabc", 无 → 0
j=7: "abaabca", "a"="a" → 1
```

### 2.2 nextval 数组（优化版）

**优化思想**：如果跳转后 `pattern[next[j]] == pattern[j]`，则跳了也还是会失败，应继续跳。

**手算 nextval**（模式串: `"abaabcac"`）：

```
j:       0    1    2    3    4    5    6    7
字符:    a    b    a    a    b    c    a    c
next:   -1    0    0    1    1    2    0    1
nextval:-1    0   -1    1    0    2   -1    1

规则:
  nextval[0] = -1
  若 pattern[next[j]] == pattern[j]:
      nextval[j] = nextval[next[j]]   # 继续跳
  否则:
      nextval[j] = next[j]            # 不需优化
```

### 2.3 KMP 匹配过程

**手写匹配过程**（主串: `"aaaaab"`，模式串: `"aab"`，next=[-1,0,1]）：

```
主串:   a a a a a b
模式串: a a b          next = [-1, 0, 1]

步骤1: i=0 j=0  'a'='a' ✓  i++, j++
步骤2: i=1 j=1  'a'='a' ✓  i++, j++
步骤3: i=2 j=2  'a'≠'b' ✗  j=next[2]=1 (i不动!)
步骤4: i=2 j=1  'a'='a' ✓  i++, j++
步骤5: i=3 j=2  'a'≠'b' ✗  j=next[2]=1
步骤6: i=3 j=1  'a'='a' ✓  i++, j++
步骤7: i=4 j=2  'a'≠'b' ✗  j=next[2]=1
步骤8: i=4 j=1  'a'='a' ✓  i++, j++
步骤9: i=5 j=2  'b'='b' ✓  j==m, 匹配成功! 位置=5-3=3
```

> 对比 BF：主串 i 从不回溯，效率更高

**Python 实现**：

```python
def get_next(pattern):
    """求 next 数组"""
    m = len(pattern)
    next_arr = [0] * m
    next_arr[0] = -1
    if m == 1:
        return next_arr
    next_arr[1] = 0
    j, k = 2, 0
    while j < m:
        if k == -1 or pattern[j - 1] == pattern[k]:
            k += 1
            next_arr[j] = k
            j += 1
        else:
            k = next_arr[k]
    return next_arr

def get_nextval(pattern, next_arr):
    """求 nextval 数组 (优化版)"""
    m = len(pattern)
    nextval = [0] * m
    nextval[0] = -1
    for j in range(1, m):
        if next_arr[j] != -1 and pattern[next_arr[j]] == pattern[j]:
            nextval[j] = nextval[next_arr[j]]
        else:
            nextval[j] = next_arr[j]
    return nextval

def kmp_search(text, pattern):
    """KMP 模式匹配 O(m+n)"""
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    next_arr = get_next(pattern)
    i = j = 0
    while i < n and j < m:
        if j == -1 or text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            j = next_arr[j]  # j 跳转, i 不回溯!
    if j == m:
        return i - m
    return -1
```

---

## 3. 更多 next 数组手算练习

**练习1**（模式串: `"ababaaab"`）：

```
j:      0    1    2    3    4    5    6    7
字符:   a    b    a    b    a    a    a    b
next:  -1    0    0    1    2    3    1    1
```

**练习2**（模式串: `"abcabd"`）：

```
j:      0    1    2    3    4    5
字符:   a    b    c    a    b    d
next:  -1    0    0    0    1    2
```

> 💡 **手算技巧**: 看 `pattern[0..j-1]` 中，最长的**既是前缀又是后缀**的子串长度

---

## 🧠 考研重点速记

### 朴素匹配
- **时间**: O(m×n)
- 匹配失败 i 回溯到 `i - j + 2`（1-indexed）
- 最好情况 O(n)：每次第一个字符就失败

### KMP 算法
- **时间**: O(m+n)
- **核心**: i 不回溯，j 按 next 数组跳转
- **next[j]** = `pattern[0..j-1]` 最长公共前后缀长度
- `next[0] = -1`，`next[1] = 0`

### nextval 优化
- 若 `pattern[next[j]] == pattern[j]`，跳了也白跳
- `nextval[j] = nextval[next[j]]`

### 手算要求
- **手算 next/nextval**: 考研必考，务必熟练!
- 看 `pattern[0..j-1]` 中，最长的既是前缀又是后缀的子串长度

---

## 📁 文件结构

```
4_string/
├── README.md                 # 本文档
└── 4_1_pattern_matching.py   # 朴素匹配/KMP/next/nextval
```

每个 Python 文件包含：
- 📝 算法说明文档字符串
- ⚡ 标准实现函数
- 🔍 带详细输出的 verbose 版本
- ✍️ next 数组手算演示
- ✅ 测试用例

运行示例：
```bash
python 4_string/4_1_pattern_matching.py
```
