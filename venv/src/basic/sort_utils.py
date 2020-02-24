import time

"""
插入排序（英语：Insertion Sort）
    是一种简单直观的排序算法。它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。
插入排序的时间复杂度问题
    最优时间复杂度：O(n) （升序排列，序列已经处于升序状态）
    最坏时间复杂度：O(n2)
    稳定性：稳定
[11,13,12,5,6]
    [11,13,12,5,6]
    [11,13,12,5,6]
    [11,12,13,5,6]
    [11,12,5,13,6]
    [11,5,12,13,6]
    [5,11,12,13,6]
    [5,11,12,6,13]
    [5,11,6,12,13]
    [5,6,11,12,13]
"""
def insertion_sort (data_list) :
    begin = 1
    end = len(data_list)
    counter = 1
    for i in range(begin, end) :
        k = data_list[i]
        while k < data_list[i - 1] and i > 0 :
            data_list[i] = data_list[i - 1]
            data_list[i - 1] = k
            i -= 1
            counter += 1
    #print(data_list)
    return data_list, counter

"""
快速排序使用分治法（Divide and conquer）策略来把一个序列（list）分为较小和较大的2个子序列，然后递归地排序两个子序列。
步骤为：
    挑选基准值：从数列中挑出一个元素，称为"基准"（pivot）;
    分割：重新排序数列，所有比基准值小的元素摆放在基准前面，所有比基准值大的元素摆在基准后面（与基准值相等的数可以到任何一边）。在这个分割结束之后，对基准值的排序就已经完成;
    递归排序子序列：递归地将小于基准值元素的子序列和大于基准值元素的子序列排序。
递归到最底部的判断条件是数列的大小是零或一，此时该数列显然已经有序。
选取基准值有数种具体方法，此选取方法对排序的时间性能有决定性影响。
"""
def quick_sort(data_list) :
    if len(data_list) <= 1 :
        return data_list
    pivot = data_list[len(data_list) // 2]  # 挑选基准值
    left = [x for x in data_list if x < pivot]  # 取小于基准值的数放在左边的元组
    middle = [x for x in data_list if x == pivot]
    right = [x for x in data_list if x > pivot]     # 取大于基准值的数放在左边的元组
    return quick_sort(left) + middle + quick_sort(right)

"""
选择排序算法：
选择排序（Selection sort）是一种简单直观的排序算法。
首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置，然后，再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。以此类推，直到所有元素均排序完毕。
"""
def selection_sort(data_list) :
    start_time = time.time() * 1000
    for i in range(len(data_list)) :
        min_idx = i
        for j in range(i + 1, len(data_list)) :
            if (data_list[j] < data_list[min_idx]) :
                min_idx = j
        data_list[i], data_list[min_idx] = data_list[min_idx], data_list[i]
    end_time = time.time() * 1000
    print("selection sort takes {} millis.".format(end_time - start_time))
    return data_list

"""
冒泡排序（Bubble Sort）也是一种简单直观的排序算法。
它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。
走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。
这个算法的名字由来是因为越小的元素会经由交换慢慢"浮"到数列的顶端。
"""
def bubble_sort(data_list) :
    n = len(data_list)
    start_time = time.time() * 1000
    for i in range(n) :
        for j in range(n - i - 1) :
            if (data_list[j] > data_list[j + 1]) :
                data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
    end_time = time.time() * 1000
    print("bubble sort takes {} millis.".format(end_time - start_time))
    return data_list
