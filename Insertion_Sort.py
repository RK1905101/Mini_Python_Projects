def insertion_sort(nums):
    n=len(nums)
    for i in range(1, n):
        k = nums[i]
        j = i-1
        while j >= 0 and nums[j]>k:
            nums[j+1] = nums[j]
            j -= 1
        nums[j+1] = k
    return nums


if __name__=='__main__':
    l=[3,6,7,45,23,14,1,20]
    print(insertion_sort(l))
