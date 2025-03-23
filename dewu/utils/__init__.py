import time


class Limiter:
    def __init__(self, requests_per_second):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    def is_ok(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request >= self.min_interval:
            self.last_request_time = current_time
            return True
        else:
            return False

    def time_until_reset(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        return max(0.0, self.min_interval - time_since_last_request)

