# 第8章 排序

> **考研要点速排序**：快速排序、堆排序、归并排序是考研重点；冒泡、插入、选择排序要会写代码；排序算法的稳定性要记住。

## 1. 插入排序类 <a id="insertion"></a>

### 直接插入排序

**原理**：将待排元素依次插入到已排序列的合适位置，类似打牌整理手牌。

```python
def insertion_sort(arr: list) -> None:
    """
    直接插入排序
    时间复杂度：最好O(n)，平均O(n²)，最坏O(n²)
    空间复杂度：O(1)
    稳定性：稳定
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # 将大于key的元素后移
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key
```

**手工推导**：
```
初始: [5, 2, 4, 6, 1, 3]
i=1:  [2, 5, 4, 6, 1, 3]  (2插入5前面)
i=2:  [2, 4, 5, 6, 1, 3]  (4插入5前面)
i=3:  [2, 4, 5, 6, 1, 3]  (6已在正确位置)
i=4:  [1, 2, 4, 5, 6, 3]  (1插入最前面)
i=5:  [1, 2, 3, 4, 5, 6]  (3插入4前面)
```

### 希尔排序

**原理**：分组插入排序，按增量gap将数组分组，对每组插入排序，逐步缩小gap直到1。

```python
def shell_sort(arr: list) -> None:
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

            # 组内插入排序
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp
        gap //= 2
```

## 2. 交换排序类 <a id="exchange"></a>

### 冒泡排序

**原理**：反复比较相邻元素，逆序则交换，每次将最大元素"冒泡"到末尾。

```python
def bubble_sort(arr: list) -> None:
    """
    冒泡排序
    时间复杂度：最好O(n)，平均O(n²)，最坏O(n²)
    空间复杂度：O(1)
    稳定性：稳定
    """
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # 若本轮无交换，已有序
        if not swapped:
            break
```

### 快速排序

**原理**：选一个"枢轴"，将小于枢轴的放左边，大于枢轴的放右边，递归处理左右子数组。

```python
def quick_sort(arr: list) -> None:
    """
    快速排序
    时间复杂度：最好O(nlogn)，平均O(nlogn)，最坏O(n²)
    空间复杂度：O(logn)递归栈
    稳定性：不稳定
    """
    def partition(low: int, high: int) -> int:
        """分区函数，返回枢轴最终位置"""
        pivot = arr[high]  # 选最后一个元素为枢轴
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort_helper(low: int, high: int) -> None:
        if low < high:
            pi = partition(low, high)
            quick_sort_helper(low, pi - 1)
            quick_sort_helper(pi + 1, high)

    quick_sort_helper(0, len(arr) - 1)
```

## 3. 选择排序类 <a id="selection"></a>

### 简单选择排序

**原理**：每次从未排序部分选出最小元素，放到已排序部分末尾。

```python
def selection_sort(arr: list) -> None:
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
```

### 堆排序

**原理**：将数组建成大顶堆，反复取出堆顶（最大元素），调整堆。

```python
def heap_sort(arr: list) -> None:
    """
    堆排序
    时间复杂度：最好O(nlogn)，平均O(nlogn)，最坏O(nlogn)
    空间复杂度：O(1)
    稳定性：不稳定
    """
    n = len(arr)

    def heapify(size: int, root: int) -> None:
        """堆化"""
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right

        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(size, largest)

    # 建堆（从最后一个非叶子节点开始）
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # 排序：每次取出堆顶，缩小堆规模
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
```

## 4. 归并 & 基数排序 <a id="merge-radix"></a>

### 归并排序

**原理**：将数组分成两半，递归排序，合并两个有序子数组。

```python
def merge_sort(arr: list) -> None:
    """
    归并排序
    时间复杂度：最好O(nlogn)，平均O(nlogn)，最坏O(nlogn)
    空间复杂度：O(n)
    稳定性：稳定
    """
    def merge(left: int, mid: int, right: int) -> None:
        """合并两个有序子数组"""
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

    def merge_sort_helper(left: int, right: int) -> None:
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(left, mid)
            merge_sort_helper(mid + 1, right)
            merge(left, mid, right)

    merge_sort_helper(0, len(arr) - 1)
```

### 基数排序

**原理**：按个位、十位、百位...依次进行稳定排序（通常用计数排序）。

```python
def counting_sort(arr: list, exp: int) -> None:
    """按指定位数进行计数排序"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # 统计出现次数
    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    # 累加，计算位置
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 构建输出数组（从右向左，保证稳定性）
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # 复制回原数组
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr: list) -> None:
    """
    基数排序（假设是非负整数）
    时间复杂度：O(d(n+r))，d为位数，r为基数(10)
    空间复杂度：O(n+r)
    稳定性：稳定
    """
    if not arr:
        return

    # 找最大值确定位数
    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
```

### 计数排序

**原理**：统计每个值出现的次数，按次数恢复数组。

```python
def counting_sort_simple(arr: list) -> None:
    """
    计数排序（假设元素范围0-99）
    时间复杂度：O(n+k)，k为元素范围大小
    空间复杂度：O(k)
    稳定性：稳定
    """
    if not arr:
        return

    k = max(arr) + 1
    count = [0] * k

    # 统计
    for num in arr:
        count[num] += 1

    # 恢复
    idx = 0
    for i in range(k):
        while count[i] > 0:
            arr[idx] = i
            idx += 1
            count[i] -= 1
```

## 5. 排序算法比较 <a id="comparison"></a>

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定性 | 适用场景 |
|------|------|------|------|------|--------|---------|
| 直接插入 | O(n) | O(n²) | O(n²) | O(1) | ✅稳定 | 基本有序，小规模 |
| 希尔 | O(n) | O(n^1.3) | O(n²) | O(1) | ❌不稳定 | 中等规模 |
| 冒泡 | O(n) | O(n²) | O(n²) | O(1) | ✅稳定 | 小规模 |
| 快速排序 | O(nlogn) | O(nlogn) | O(n²) | O(logn) | ❌不稳定 | 大规模，平均性能好 |
| 简单选择 | O(n²) | O(n²) | O(n²) | O(1) | ❌不稳定 | 小规模 |
| 堆排序 | O(nlogn) | O(nlogn) | O(nlogn) | O(1) | ❌不稳定 | 大规模，需要稳定的最坏性能 |
| 归并排序 | O(nlogn) | O(nlogn) | O(nlogn) | O(n) | ✅稳定 | 要求稳定，外部排序 |
| 计数排序 | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅稳定 | 整数，范围小 |
| 基数排序 | O(d(n+r)) | O(d(n+r)) | O(d(n+r)) | O(r) | ✅稳定 | 多关键字排序 |

## 考研重点 & 易错点

- ⚠️ 易错点：快速排序最坏O(n²)发生在数组已有序且每次选最右为枢轴
- 📌 高频考点：堆排序的建堆过程从最后一个非叶子节点开始调整（n/2-1到0）
- ⚠️ 易错点：希尔排序的gap选择影响性能，常用gap序列：n/2, n/4, ..., 1
- 📌 高频考点：排序算法的稳定性记忆，只有插入、冒泡、归并、计数、基数是稳定的
- 📌 高频考点：选择排序的不稳定性示例：[5, 5', 3] → [3, 5', 5]，两个5的相对位置改变

## 代码示例：运行所有排序算法

```python
if __name__ == "__main__":
    test_arr = [5, 2, 4, 6, 1, 3]
    print(f"原始数组: {test_arr}")

    # 测试各排序算法
    for sort_func in [
        insertion_sort, bubble_sort, selection_sort,
        shell_sort, quick_sort, heap_sort, merge_sort,
        counting_sort_simple, radix_sort
    ]:
        arr = test_arr.copy()
        sort_func(arr)
        print(f"{sort_func.__name__}: {arr}")
```
