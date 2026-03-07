# 第8章 排序

> 本章包含9种常见排序算法的完整总结，涵盖算法思想、复杂度分析、手写排序过程和Python实现。适合408考研数据结构复习使用。

---

## 📊 算法对比总览 <a id="comparison"></a>

| 算法 | 平均时间 | 最坏时间 | 空间 | 稳定性 |
|------|---------|---------|------|-------|
| 冒泡排序 | O(n²) | O(n²) | O(1) | ✅ 稳定 |
| 直接插入排序 | O(n²) | O(n²) | O(1) | ✅ 稳定 |
| 简单选择排序 | O(n²) | O(n²) | O(1) | ❌ 不稳定 |
| 希尔排序 | O(n log n)~O(n²) | O(n²) | O(1) | ❌ 不稳定 |
| 快速排序 | O(n log n) | O(n²) | O(log n) | ❌ 不稳定 |
| 归并排序 | O(n log n) | O(n log n) | O(n) | ✅ 稳定 |
| 堆排序 | O(n log n) | O(n log n) | O(1) | ❌ 不稳定 |
| 计数排序 | O(n+k) | O(n+k) | O(k) | ✅ 稳定 |
| 基数排序 | O(d·(n+k)) | O(d·(n+k)) | O(n+k) | ✅ 稳定 |

> **助记**：稳定的排序 → **"冒插归计基"**（冒泡、插入、归并、计数、基数）

---

## 1. 冒泡排序 (Bubble Sort) <a id="exchange"></a>

**核心思想**：相邻元素两两比较，较大的像气泡一样向右"冒"，每轮结束后最大值沉到末尾。若某轮未发生交换则提前结束。

**关键步骤**：
1. 外层循环 `i` 控制轮次（共 n-1 轮）
2. 内层 `j` 从 0 扫到 `n-i-2`，比较 `arr[j]` 与 `arr[j+1]`
3. 若 `arr[j] > arr[j+1]` 则交换
4. 设 `swapped` 标记，若整轮无交换则提前 break

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始        → [5, 3, 8, 1, 9, 2]
第1轮 i=0   → [3, 5, 1, 8, 2, 9]   9 冒到末尾
第2轮 i=1   → [3, 1, 5, 2, 8, 9]   8 到位
第3轮 i=2   → [1, 3, 2, 5, 8, 9]   5 到位
第4轮 i=3   → [1, 2, 3, 5, 8, 9]   3 到位
完成        → [1, 2, 3, 5, 8, 9]
```

**Python 实现**：

```python
def bubble_sort(arr):
    """
    冒泡排序
    时间复杂度：最好O(n)，平均O(n²)，最坏O(n²)
    空间复杂度：O(1)
    稳定性：稳定
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

---

## 2. 直接插入排序 (Insertion Sort) <a id="insertion"></a>

**核心思想**：类似抓扑克牌。左侧维护已排序区，每次取右侧第一个元素，向左找到合适位置插入，其余元素右移一位。

**关键步骤**：
1. 从 `i=1` 开始，取 `key = arr[i]`
2. `j` 从 `i-1` 向左扫，`arr[j] > key` 则 `arr[j+1]=arr[j]`，`j--`
3. 退出循环后，`arr[j+1] = key`
4. 每插入一次，有序区扩大一位

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始        → [5, 3, 8, 1, 9, 2]
i=1 插入3   → [3, 5, 8, 1, 9, 2]   3 插到 5 前
i=2 插入8   → [3, 5, 8, 1, 9, 2]   8 不动
i=3 插入1   → [1, 3, 5, 8, 9, 2]   1 插到最前
i=4 插入9   → [1, 3, 5, 8, 9, 2]   9 不动
i=5 插入2   → [1, 2, 3, 5, 8, 9]   2 插到第2位
```

**Python 实现**：

```python
def insertion_sort(arr):
    """
    直接插入排序
    时间复杂度：最好O(n)，平均O(n²)，最坏O(n²)
    空间复杂度：O(1)
    稳定性：稳定
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

---

## 3. 简单选择排序 (Selection Sort) <a id="selection"></a>

**核心思想**：每轮在未排序区找最小值，与未排序区首元素交换。交换次数最少（≤n-1次），但比较次数固定 n(n-1)/2，不因有序而提前结束。

**关键步骤**：
1. 外层 `i` 从 0 到 `n-2`，表示当前待填位置
2. 内层 `j` 从 `i+1` 扫到末尾，记录最小值下标 `min_idx`
3. 交换 `arr[i]` 与 `arr[min_idx]`
4. 已排序区扩大，**不稳定**（交换可能越过相同元素）

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始          → [5, 3, 8, 1, 9, 2]
i=0 找最小=1  → [1, 3, 8, 5, 9, 2]  1(idx3) ↔ 5(idx0)
i=1 找最小=2  → [1, 2, 8, 5, 9, 3]  2(idx5) ↔ 3(idx1)
i=2 找最小=3  → [1, 2, 3, 5, 9, 8]  3(idx5) ↔ 8(idx2)
i=3 找最小=5  → [1, 2, 3, 5, 9, 8]  5 不动
完成          → [1, 2, 3, 5, 8, 9]
```

**Python 实现**：

```python
def selection_sort(arr):
    """
    简单选择排序
    时间复杂度：最好O(n²)，平均O(n²)，最坏O(n²)
    空间复杂度：O(1)
    稳定性：不稳定
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

---

## 4. 希尔排序 (Shell Sort)

**核心思想**：插入排序的改进。先用大步长分组插排，使元素快速靠近目标；步长逐渐缩小至1，最后一次完整插排时数组已近乎有序，代价极小。

**关键步骤**：
1. 初始 `gap = n//2`，每轮结束 `gap //= 2`
2. 对每个 gap，从 `i=gap` 开始做插入排序（跨度为 gap）
3. 重复直到 `gap=1` 完成最终插排
4. 步长序列影响性能，常用 `n//2, n//4...` 或 Knuth 序列

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`, n=6）：

```
初始 [n=6]    → [5, 3, 8, 1, 9, 2]  gap从3开始
gap=3 分组    → [1, 3, 8, 5, 9, 2]  [5,1],[3,9],[8,2] 各自插排
gap=3 结果    → [1, 3, 2, 5, 9, 8]  整体接近有序
gap=1 插排    → [1, 2, 3, 5, 8, 9]  代价很小
```

**Python 实现**：

```python
def shell_sort(arr):
    """
    希尔排序
    时间复杂度：最好O(n)，平均O(n^1.3)，最坏O(n²)
    空间复杂度：O(1)
    稳定性：不稳定
    """
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
```

---

## 5. 快速排序 (Quick Sort)

**核心思想**：分治策略。选末尾元素为 pivot，partition 后 pivot 左边全 ≤ pivot，右边全 > pivot，pivot 归位。递归处理两侧。最坏情况（有序数组）退化 O(n²)。

**关键步骤**：
1. `partition`：`i=low-1`，`j` 遍历 `low~high-1`
2. `arr[j] ≤ pivot` 时 `i++`，交换 `arr[i]` 和 `arr[j]`
3. 循环结束，交换 `arr[i+1]` 和 `arr[high]`，返回 `i+1`
4. 递归对 `[low, pi-1]` 和 `[pi+1, high]` 排序

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始        → [5, 3, 8, 1, 9, 2]  pivot=2(末尾)
partition   → [1, 2, 8, 5, 9, 3]  2 归位 idx=1
左递归      → [1, 2, 8, 5, 9, 3]  [1] 归位
右递归      → [1, 2, 3, 5, 8, 9]  [8,5,9,3] 继续分
完成        → [1, 2, 3, 5, 8, 9]
```

**Python 实现**：

```python
def quick_sort(arr, low=0, high=None):
    """
    快速排序
    时间复杂度：最好O(nlogn)，平均O(nlogn)，最坏O(n²)
    空间复杂度：O(logn)递归栈
    稳定性：不稳定
    """
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

## 6. 归并排序 (Merge Sort) <a id="merge-radix"></a>

**核心思想**：分治策略。不断二分到单个元素（自然有序），再两两合并有序段。合并时双指针取小者填入。唯一能保证最坏 O(n log n) 的比较排序，代价是需要 O(n) 额外空间。

**关键步骤**：
1. 递归拆分：`mid = (lo+hi)//2`，分别排左右两半
2. 合并：`left[i]` 与 `right[j]` 比较，取小者放入 output
3. 剩余部分直接追加
4. 写回原数组对应区间

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始        → [5, 3, 8, 1, 9, 2]
拆分到底    → [5][3][8][1][9][2]
两两合并    → [3,5][1,8][2,9]
四合并二    → [1,3,5,8][2,9]
完成        → [1, 2, 3, 5, 8, 9]
```

**Python 实现**：

```python
def merge_sort(arr):
    """
    归并排序
    时间复杂度：最好O(nlogn)，平均O(nlogn)，最坏O(nlogn)
    空间复杂度：O(n)
    稳定性：稳定
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result
```

---

## 7. 堆排序 (Heap Sort)

**核心思想**：两阶段：① 建大根堆（从最后非叶节点向上 heapify）；② 反复将堆顶（最大值）与末尾交换，堆大小减1，再对新堆顶 heapify。原地排序，不稳定。

**关键步骤**：
1. 建堆：`i` 从 `n//2-1` 到 0，对每个 `i` 执行 `heapify`
2. `heapify`：找左右孩子中最大者，若大于父节点则交换，递归下沉
3. 排序：交换 `arr[0]` 和 `arr[i]`（`i` 从 `n-1` 到 1），对 `arr[0]` heapify
4. 每次交换后有序区扩大一位

**手写排序过程**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始          → [5, 3, 8, 1, 9, 2]   先建大根堆
建堆完成      → [9, 5, 8, 1, 3, 2]   堆顶=最大值9
交换堆顶↔末   → [2, 5, 8, 1, 3, 9]   9 归位，堆大小-1
heapify后     → [8, 5, 2, 1, 3, 9]   8 成新堆顶
再交换        → [3, 5, 2, 1, 8, 9]   8 归位
完成          → [1, 2, 3, 5, 8, 9]
```

**Python 实现**：

```python
def heap_sort(arr):
    """
    堆排序
    时间复杂度：最好O(nlogn)，平均O(nlogn)，最坏O(nlogn)
    空间复杂度：O(1)
    稳定性：不稳定
    """
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr

def heapify(arr, n, i):
    largest = i
    l, r = 2*i+1, 2*i+2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

---

## 8. 计数排序 (Counting Sort)

**核心思想**：非比较排序。统计每个值出现次数，前缀和得出各值的最终位置，反向遍历原数组写入输出（反向保证稳定）。k 为值域范围，k 过大时不适用。

**关键步骤**：
1. `count[v-min]++` 统计每个值频次
2. 前缀和：`count[i] += count[i-1]`，得排名
3. 反向遍历原数组：`output[count[v]-1]=v`，`count[v]--`
4. output 写回 arr

**手写排序过程**（初始: `[3, 1, 4, 1, 5, 2]`，值域 1~5, k=5）：

```
初始     → [3, 1, 4, 1, 5, 2]  值域 1~5，k=5
计数     → count=[2,1,1,1,1]   (1出现2次)
前缀和   → count=[2,3,4,5,6]
回填     → [1, 1, 2, 3, 4, 5]  按位置写入
```

**Python 实现**：

```python
def counting_sort(arr):
    """
    计数排序
    时间复杂度：O(n+k)
    空间复杂度：O(k)
    稳定性：稳定
    """
    if not arr:
        return arr
    max_val = max(arr)
    min_val = min(arr)
    k = max_val - min_val + 1
    count = [0] * k
    for num in arr:
        count[num - min_val] += 1
    for i in range(1, k):
        count[i] += count[i - 1]
    output = [0] * len(arr)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
    return output
```

---

## 9. 基数排序 (Radix Sort)

**核心思想**：非比较排序。LSD（低位优先）：从个位到最高位，每轮对该位做稳定的计数排序（10个桶）。d 轮后得到有序结果。依赖稳定子排序保证正确性。

**关键步骤**：
1. `exp=1` 表示当前处理的位（个位十位…）
2. 按 `(num // exp) % 10` 做计数排序（10个桶）
3. 反向写回保证稳定性
4. `exp *= 10`，直到最高位处理完毕

**手写排序过程**（初始: `[170, 45, 75, 90, 2, 24]`，d=3位）：

```
初始       → [170,  45,  75,  90,   2,  24]  d=3位
按个位排   → [170,  90,   2,  24,  45,  75]  0,0,2,4,5,5
按十位排   → [  2,  24,  45,  75, 170,  90]  0,2,4,7,7,9
按百位排   → [  2,  24,  45,  75,  90, 170]  0,0,0,0,0,1
```

**Python 实现**：

```python
def radix_sort(arr):
    """
    基数排序
    时间复杂度：O(d·(n+k))
    空间复杂度：O(n+k)
    稳定性：稳定
    """
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for num in reversed(arr):
        digit = (num // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1
    for i in range(n):
        arr[i] = output[i]
```

---

## 🧠 考研重点速记

### 稳定性判断

| 稳定 | 不稳定 |
|------|-------|
| 冒泡、插入、归并 | 选择、希尔、快排、堆排 |
| 计数、基数 | |

> 口诀：**"快些选堆"不稳定**（快排、希尔、选择、堆排）

### 最坏时间 O(n log n) 的排序
- **归并排序**、**堆排序**（任何输入都是 O(n log n)）

### 最好时间 O(n) 的排序
- **冒泡排序**（有序 + swapped 优化）
- **插入排序**（有序时只需 n-1 次比较）

### 空间复杂度

| O(1) 原地 | O(log n) | O(n) |
|-----------|----------|------|
| 冒泡、插入、选择 | 快排（栈） | 归并 |
| 希尔、堆排 | | 计数、基数 |

### 适用场景
- **小规模/基本有序** → 插入排序
- **大规模通用** → 快速排序（平均最快）
- **要求稳定 + 大规模** → 归并排序
- **值域小整数** → 计数排序
- **多关键字/大整数** → 基数排序
- **原地 + 保证 O(n log n)** → 堆排序

---

## 📝 代码示例：运行所有排序算法

```python
if __name__ == "__main__":
    test_arr = [5, 3, 8, 1, 9, 2]
    print(f"原始数组: {test_arr}")

    # 测试各排序算法
    for sort_func in [
        bubble_sort, insertion_sort, selection_sort,
        shell_sort, quick_sort, heap_sort, merge_sort,
        counting_sort
    ]:
        arr = test_arr.copy()
        result = sort_func(arr) if sort_func != quick_sort else sort_func(arr[:])
        print(f"{sort_func.__name__}: {result}")
```
