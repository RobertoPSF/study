def max_subarray_sum_k(nums, k):
    if (len(nums)) < k:
        return None
    
    current_sum = sum(nums[:k])
    max_sum = current_sum

    for i in range(k, len(nums)):
        current_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, current_sum)

    return max_sum


def are_anagram(s,t):

    if len(s) != len(t):
        return False
    
    count = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}

    for c in s:
        count[c] += 1

    for c in t:
        count[c] -= 1
        if count[c] < 0:
            return False
        
    return True


def analyze_data(nums, k, s, t):
    return {"maxSubarraySum":max_subarray_sum_k(nums, k), "areAnagram": are_anagram(s, t)}


nums = [2, 1, 5, 1, 3, 2]
k = 3
s = "listen"
t = "silent"

print(analyze_data(nums, k, s, t))