MIN_MERGE = 32


def calc_min_run(n):
    """返回一个范围在23-64之间的最小运行长度，使得len(array)/minrun小于等于2的幂次方。"""
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def binary_insertion_sort(a, left, right):
    """二分插入排序，用于对数组的部分进行排序。"""
    for i in range(left + 1, right + 1):
        key = a[i]
        pos = binary_search(a, key, left, i)

        # 将从“pos”到“i-1”的所有元素向右移动一步
        j = i - 1
        while j >= pos:
            a[j + 1] = a[j]
            j -= 1
        a[pos] = key


def binary_search(a, key, left, right):
    """二分查找函数，用于找到可以插入key的位置。"""
    while left < right:
        mid = left + (right - left) // 2
        if a[mid] < key:
            left = mid + 1
        else:
            right = mid
    return left


def merge(arr, left, mid, right):
    """合并函数，用于合并数组的两个已排序部分。"""
    # 根据情况切换合并方向，以避免额外的复制
    if mid - left > right - mid:
        left_part = arr[left : mid + 1]
        i, j, k = len(left_part) - 1, mid + 1, right
        while i >= 0 and j <= k:
            if left_part[i] > arr[j]:
                arr[k] = left_part[i]
                i -= 1
            else:
                arr[k] = arr[j]
                j += 1
            k -= 1
        if i >= 0:  # left_part中剩余的元素
            arr[left : k + 1] = left_part[: i + 1]
    else:
        right_part = arr[mid + 1 : right + 1]
        i, j, k = mid, len(right_part) - 1, left
        while i >= left and j >= 0:
            if arr[i] > right_part[j]:
                arr[k] = arr[i]
                i -= 1
            else:
                arr[k] = right_part[j]
                j -= 1
            k += 1
        if j >= 0:  # right_part中剩余的元素
            arr[k : k + j + 1] = right_part[: j + 1]


def timsort(arr):
    n = len(arr)
    min_run = calc_min_run(n)

    # 使用二分插入排序对大小为min_run的子数组进行排序
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        binary_insertion_sort(arr, start, end)

    # 从大小为min_run（或n）开始合并。它将合并
    # 形成大小为2 * min_run，然后是4 * min_run，8 * min_run等等...
    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            mid = min((start + size - 1), (n - 1))
            end = min((start + 2 * size - 1), (n - 1))
            if mid < end:
                merge(arr, start, mid, end)
        size *= 2

    return arr


# 示例用法：
arr = [5, 9, 1, 3, 4, 6, 6, 3, 2]
arr = timsort(arr)
print(arr)
