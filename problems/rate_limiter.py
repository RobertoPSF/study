class RateLimiter:

    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.user_requests = {}
        

    def allow_request(self, user_id: str, timestamp: int) -> bool:
        print(self.user_requests)
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        while self.user_requests[user_id] and self.user_requests[user_id][0] <= timestamp - self.time_window:
            self.user_requests[user_id].pop(0)

        if len(self.user_requests[user_id]) < self.max_requests:
            self.user_requests[user_id].append(timestamp)
            return True
        
        else:
            return False
        
rate_limiter = RateLimiter(3, 10)

print(rate_limiter.allow_request("user1", 1))
print(rate_limiter.allow_request("user1", 2))
print(rate_limiter.allow_request("user1", 3))
print(rate_limiter.allow_request("user1", 5))
print(rate_limiter.allow_request("user1", 11))