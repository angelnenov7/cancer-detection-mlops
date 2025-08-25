from fastapi import Request
import time
from statistics import mean
import logging

logger = logging.getLogger("performance")

class PerformanceMiddleware:
    def __init__(self):
        self.response_times = []
        
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        self.response_times.append(duration)
        if len(self.response_times) > 100:
            self.response_times.pop(0)
            
        logger.info(f"Path: {request.url.path} Duration: {duration:.3f}s "
                   f"Avg (last 100): {mean(self.response_times):.3f}s")
        
        return response