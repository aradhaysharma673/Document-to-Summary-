from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time
from app.config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limit for health check
        if request.url.path == "/health":
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < settings.rate_limit_window
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= settings.rate_limit_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {settings.rate_limit_requests} requests per {settings.rate_limit_window} seconds."
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Add remaining requests to response header
        response = await call_next(request)
        remaining = settings.rate_limit_requests - len(self.requests[client_ip])
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response

class ContentSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check content length
        content_length = request.headers.get("content-length")
        
        if content_length and int(content_length) > settings.max_content_length:
            raise HTTPException(
                status_code=413,
                detail=f"Content too large. Max size: {settings.max_content_length} bytes"
            )
        
        return await call_next(request)
