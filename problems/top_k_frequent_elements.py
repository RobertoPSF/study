import heapq

def func(nums, k):
    freq = {}
    

    for num in nums:
        freq[num] = freq.get(num, 0) + 1
        
    heap = []

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)

    print(heap)
        
    return [num for _, num in heap]
    

print(func([4,4,4,6,6,7,7,7,7], 1))




