import time
from typing import Dict
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_second: int = 2):
        self.requests_per_second = requests_per_second
        self.last_request_time: Dict[str, float] = defaultdict(float)
        
    def wait(self, domain: str):
        """Wait if necessary to maintain the rate limit for the given domain"""
        current_time = time.time()
        time_passed = current_time - self.last_request_time[domain]
        
        if time_passed < (1.0 / self.requests_per_second):
            sleep_time = (1.0 / self.requests_per_second) - time_passed
            time.sleep(sleep_time)
            
        self.last_request_time[domain] = time.time() 