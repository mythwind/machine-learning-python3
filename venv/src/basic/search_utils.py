

"""
二分查找
    二分搜索是一种在有序数组中查找某一特定元素的搜索算法。搜索过程从数组的中间元素开始，如果中间元素正好是要查找的元素，则搜索过程结束；
    如果某一特定元素大于或者小于中间元素，则在数组大于或小于中间元素的那一半中查找，而且跟开始一样从中间元素开始比较。如果在某一步骤数组为空，则代表找不到。
    这种搜索算法每一次比较都使搜索范围缩小一半。
该算法的要求：
     1、必须采用顺序存储结构。
     2、必须按关键字大小有序排列
"""
def binary_search(arr, begin, end, x, counter) :
    # 返回 x 在 arr 中的索引，如果不存在返回 -1
    counter += 1
    if begin <= end :
        mid = int(begin + (end - begin) // 2)
        if arr[mid] == x :
            return mid, counter
        elif arr[mid] > x :
            return binary_search(arr, begin, mid - 1, x, counter)
        else :
            return binary_search(arr, mid + 1, end, x, counter)
    else :
        return -1, counter

def binary_search2(data_list, val) :
    # 返回 x 在 arr 中的索引，如果不存在返回 -1
    counter = 0
    low = 0
    high = len(data_list) - 1
    while low <= high:
        counter +=1
        mid = (low + high) // 2  # 中间数下标
        if data_list[mid] == val :
            return mid, counter
        elif data_list[mid] == val :
            high = mid - 1
        else :
            low = mid + 1
    else :
        return -1, (len(data_list) - 1) // 2

"""
线性查找指按一定的顺序检查数组中每一个元素，直到找到所要寻找的特定值为止。
"""
def liner_search(data_list, val) :
    counter = 0
    for num in range(0, len(data_list) - 1) :
        counter += 1
        if data_list[num] == val :
            return num, counter
    return -1, counter

def liner_search2(data_list, val) :
    index = 0
    counter = 0
    for num in data_list :
        index += 1
        counter += 1
        if num == val :
            return index, counter
    return -1, counter