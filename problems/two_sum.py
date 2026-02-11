def func(nums, target):

    complements = {}

    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in complements:
            return complements[complement],i
        complements[nums[i]] = i

    return 0, 0


print(func([2, 7, 11, 15], 9))