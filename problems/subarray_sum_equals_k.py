def func(nums, k):
    current_sum = 0
    prefix = {0:1}
    count = 0

    for num in nums:
        current_sum += num

        if current_sum - k in prefix:
            count += prefix[current_sum - k]

        prefix[current_sum] = prefix.get(current_sum, 0) + 1

    return count


print(func([1,1,1], 2))