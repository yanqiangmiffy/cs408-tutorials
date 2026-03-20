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

**核心思想**：分治策略。选 pivot 元素，partition 后 pivot 左边全 ≤ pivot，右边全 > pivot，pivot 归位。递归处理两侧。最坏情况（有序数组）退化 O(n²)。

### 为什么快排平均快，但最坏会退化

可以把 pivot 想成“裁判”，每轮都把序列切成左右两边。

- **切得均匀**：左右两边规模差不多，递归层数大约是 `log n`，每层总工作量约 `n`，所以平均是 `O(n log n)`。
- **切得很歪**：比如每次都挑到最小值或最大值，序列会变成 `n-1` 和 `0` 两部分，递归层数接近 `n`，于是退化成 `O(n^2)`。

所以快排的快，来自“分得比较均匀”；快排的风险，也来自“分得太偏”。

### 5.1 Pivot 选择策略

| Pivot 选择 | 方式 | 特点 | 考研考点 |
|-----------|------|------|----------|
| **末尾元素** | `pivot = arr[high]` | 简单易写，最坏时有序数组退化为 O(n²) | ⭐ 常考 |
| **首元素** | `pivot = arr[low]` | 同末尾，最坏时有序数组退化 | ⭐ 常考 |
| **中间元素** | `pivot = arr[(low+high)//2]` | 略优于首末 | 次常考 |
| **随机元素** | `pivot = arr[random]` | 平均情况最优，避免最坏 | 了解 |
| **三数取中** | 取首、中、末的中位数 | 实用优化，避免最坏 | 了解 |

> **王道考研提示**：手写时常用末尾或首元素作为 pivot，便于考试演示

---

### 5.2 分区策略

#### ① 王道挖坑法（Wang Dao Hole Method）

**核心思想**：用 pivot 挖一个"坑"，从两边向中间交替填坑，最后把 pivot 放入最终坑位。

```
初始: [5, 3, 8, 1, 9, 2]  pivot=arr[0]=5, 挖坑位置 low=0

第1步: 2填入坑位 → [2, 3, 8, 1, 9, □]  坑位移到 high=5
第2步: 8填入坑位 → [2, 3, □, 1, 9, 8]  坑位移到 low=2
第3步: 1填入坑位 → [2, 3, 1, □, 9, 8]  坑位移到 high=3
第4步: pivot放坑位 → [2, 3, 1, 5, 9, 8]  pivot归位 idx=3

递归: [2,3,1] 和 [9,8]
```

**王道挖坑法代码**：

```python
def partition_hole(arr, low, high):
    """王道挖坑法分区"""
    pivot = arr[low]  # 挖坑，取出 pivot
    while low < high:
        # 从右向左找比 pivot 小的元素填坑
        while low < high and arr[high] >= pivot:
            high -= 1
        arr[low] = arr[high]  # 填坑，新坑位在 high

        # 从左向右找比 pivot 大的元素填坑
        while low < high and arr[low] <= pivot:
            low += 1
        arr[high] = arr[low]  # 填坑，新坑位在 low

    arr[low] = pivot  # pivot 归位
    return low  # 返回 pivot 最终位置
```

---

#### ② Lomuto 分区（单指针正向扫描）

**核心思想**：用单指针 `i` 维护"≤ pivot"区域的边界，指针 `j` 正向扫描整个区间。

```
初始: [5, 3, 8, 1, 9, 2]  pivot=arr[high]=2
指针:  i=-1, j 从 0 扫到 5

j=0: arr[0]=5 > pivot, i不变
j=1: arr[1]=3 > pivot, i不变
j=2: arr[2]=8 > pivot, i不变
j=3: arr[3]=1 ≤ pivot, i=0, 交换 arr[0]↔arr[3] → [1,3,8,5,9,2]
j=4: arr[4]=9 > pivot, i不变

循环结束: 交换 arr[i+1]↔arr[high] → [1,2,8,5,9,3]
pivot 归位 idx=1
```

**Lomuto 分区代码**：

```python
def partition_lomuto(arr, low, high):
    """Lomuto 分区：单指针 j 正向扫描"""
    pivot = arr[high]  # pivot 取自最后一个元素
    i = low - 1  # i 维护 ≤ pivot 区域的边界

    for j in range(low, high):  # j 正向扫描
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # 交换

    # pivot 归位
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

#### ③ Hoare 分区（双指针对向夹逼）

**核心思想**：双指针 `i` 从左、`j` 从右向中间夹逼，相遇时返回边界。

```
初始: [5, 3, 8, 1, 9, 2]  pivot=arr[low]=5
指针:  i=low, j=high

第1轮: i右移找≥5 → i=0(arr[0]=5), j左移找≤5 → j=5(arr[5]=2)
       交换 arr[0]↔arr[5] → [2, 3, 8, 1, 9, 5]
第2轮: i右移找≥5 → i=2(arr[2]=8), j左移找≤5 → j=3(arr[3]=1)
       交换 arr[2]↔arr[3] → [2, 3, 1, 8, 9, 5]
第3轮: i右移找≥5 → i=3(arr[3]=8), j左移找≤5 → j=2
       i>j，退出循环

返回边界 j=2，递归 [2,3,1] 和 [8,9,5]
```

**Hoare 分区代码**：

```python
def partition_hoare(arr, low, high):
    """Hoare 分区：双指针 i/j 对向夹逼"""
    pivot = arr[low]  # pivot 取自第一个元素
    i, j = low, high

    while i <= j:
        # i 向右找 ≥ pivot 的元素
        while i <= j and arr[i] < pivot:
            i += 1
        # j 向左找 ≤ pivot 的元素
        while i <= j and arr[j] > pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    return j  # 返回分割点
```

> **注意**：Hoare 分区返回的是分割点 `j`，递归时注意边界：`[low, j]` 和 `[j+1, high]`

---

### 5.3 快速排序实现

**标准实现（Lomuto 分区 + 末尾 pivot）**：

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
    """Lomuto 分区：pivot 取自末尾元素"""
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

### 5.4 手写排序过程

**王道挖坑法示例**（初始: `[5, 3, 8, 1, 9, 2]`）：

```
初始        → [5, 3, 8, 1, 9, 2]  pivot=5(首元素)，挖坑 idx=0
第1步2填坑 → [2, 3, 8, 1, 9, □]  坑位到 idx=5
第2步8填坑 → [2, 3, □, 1, 9, 8]  坑位到 idx=2
第3步1填坑 → [2, 3, 1, □, 9, 8]  坑位到 idx=3
pivot归位   → [2, 3, 1, 5, 9, 8]  5 归位 idx=3
左递归      → [1, 2, 3, 5, 9, 8]  [2,3,1] 排序
右递归      → [1, 2, 3, 5, 8, 9]  [9,8] 排序
完成        → [1, 2, 3, 5, 8, 9]
```

---

### 5.5 考研重点速记

| 策略 | 类型 | 考研特点 |
|------|------|----------|
| **王道挖坑法** | 双指针夹逼 | ⭐⭐⭐ 王道教材标准写法，常考 |
| **Lomuto 分区** | 单指针正向 | ⭐⭐ 简单易写，适合手写 |
| **Hoare 分区** | 双指针对向 | ⭐⭐ 原始 Hoare 版本 |

> **口诀**：挖坑填坑，交替左右，最终归位

---

## 6. 归并排序 (Merge Sort) <a id="merge-radix"></a>

**核心思想**：分治策略。不断二分到单个元素（自然有序），再两两合并有序段。合并时双指针取小者填入。唯一能保证最坏 O(n log n) 的比较排序，代价是需要 O(n) 额外空间。

### 为什么归并排序稳定

归并时，左右两段本身都已经有序。

- 如果遇到相等元素，先取左边那个，再取右边那个。
- 这样相等元素的先后顺序就和原数组保持一致。

稳定性的本质，不是“没交换”，而是“相等元素的相对次序没有被打乱”。

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

### 为什么堆排序不稳定

堆排序的关键动作是“堆顶和末尾直接交换”。

- 这个交换只关心大小，不关心两个相等元素原来的前后次序。
- 一旦某个相等元素被换到另一个相等元素前面，稳定性就被破坏了。

所以堆排序虽然是 `O(n log n)` 且原地，但稳定性是它换来的代价之一。

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

## 常考题型与相关算法题

### 常考点

- 稳定性、是否原地、最好 / 平均 / 最坏复杂度对比。
- 插入、交换、选择、归并、堆、计数、基数几类排序的适用场景。
- 快速排序分区过程、堆排序建堆过程、归并排序合并过程的手写。
- Top-K、逆序对、外部排序等综合应用。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| LeetCode 912. 排序数组 | 综合排序实现 |
| [35 数组中的逆序对](/ch09-offer/35) | 归并排序统计逆序对 |
| [29 最小的K个数](/ch09-offer/29) | 堆 / 快速选择 |
| LeetCode 215. 数组中的第K个最大元素 | 快速选择 / 堆 |
| LeetCode 347. 前 K 个高频元素 | 堆与桶排序 |
| LeetCode 148. 排序链表 | 归并排序 |
