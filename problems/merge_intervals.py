def func(intervals):
    if not intervals:
        return []
    
    intervals = sorted(intervals)
    result = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start < current_end:
            current_end = max(current_end, end)
        else:
            current_start, current_end = start, end
        
        result.append([current_start, current_end])

    return result

print(func([[1,3],[2,6],[8,10],[15,18]]))
        