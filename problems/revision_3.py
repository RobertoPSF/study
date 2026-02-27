def func(nums, k):
    current_sum = 0
    count = 0
    prefix_count = {0:1}


    for x in nums:
        current_sum += x
        if (current_sum - k) in prefix_count:
            count += prefix_count[current_sum - k]
        
        prefix_count[current_sum] = prefix_count.get(current_sum, 0) + 1

    return count

print(func([1, 2, 3],3))