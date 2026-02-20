from collections import deque

def func(events, k):
    fail_count = 0
    balance = 0
    open_paren = 0

    left = 0
    max_len = 0

    for right in range(len(events)):
        char = events[right]

        if char == "F":
            fail_count += 1
        elif char == "D":
            balance += 1
        elif char == "W":
            balance -= 1
        elif char == "(":
            open_paren += 1
        elif char == ")":
            open_paren -= 1


        while (
            fail_count > k
            or balance < 0
            or open_paren < 0
        ):
            left_char = events[left]

            if left_char == "F":
                fail_count += 1
            elif left_char == "D":
                balance += 1
            elif left_char == "W":
                balance -= 1
            elif left_char == "(":
                open_paren += 1
            elif left_char == ")":
                open_paren -= 1

            left += 1

        if open_paren == 0:
            max_len = max(max_len, right - left + 1)

    return max_len


print(func("D(DW)WFDD", 1))
