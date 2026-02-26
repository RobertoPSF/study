def func(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] > target:
            right = mid -1 
        elif nums[mid] < target:
            left = mid + 1
        else:
            return mid
        
    return -1


print(func([-1,0,3,5,9,12],9))