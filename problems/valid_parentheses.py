from collections import deque

def func(s):

    stack = deque()
    pairs = {
        ")": "(",
        "}": "{",
        "]": "["
    }

    for c in s:
        if c in ["(", "{", "["]:
            stack.append(c)
        if c in [")", "}", "]"]:
            if not stack:
                return False
            if stack[-1] != pairs[c]:
                return False
            stack.pop()

    return True

print(func("()[]{}"))