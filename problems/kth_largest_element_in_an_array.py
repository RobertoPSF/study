import heapq

def func(nums, k):

    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]

print(func([3,2,1,5,6,4], 2))