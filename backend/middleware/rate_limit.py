#!/usr/bin/env python3
"""
API Rate Limiting Middleware
Enforces subscription-based rate limits
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from collections import defaultdict
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.request_counts = defaultdict(lambda: {'count': 0, 'reset_time': time.time() + 3600})
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for non-API routes
        if not request.url.path.startswith('/api/'):
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get('X-API-Key')
        
        if api_key:
            # Check rate limit
            current_time = time.time()
            user_data = self.request_counts[api_key]
            
            # Reset counter if time window passed
            if current_time > user_data['reset_time']:
                user_data['count'] = 0
                user_data['reset_time'] = current_time + 3600  # 1 hour window
            
            # Increment counter
            user_data['count'] += 1
            
            # Get user's rate limit (from API key DB)
            # For now, default to 100/hour
            rate_limit = 100  # This should be fetched from subscription data
            
            if user_data['count'] > rate_limit:
                raise HTTPException(
                    status_code=429,
                    detail={
                        'error': 'Rate limit exceeded',
                        'limit': rate_limit,
                        'reset_at': datetime.fromtimestamp(user_data['reset_time']).isoformat()
                    }
                )
            
            # Add rate limit headers to response
            response = await call_next(request)
            response.headers['X-RateLimit-Limit'] = str(rate_limit)
            response.headers['X-RateLimit-Remaining'] = str(max(0, rate_limit - user_data['count']))
            response.headers['X-RateLimit-Reset'] = str(int(user_data['reset_time']))
            
            return response
        
        return await call_next(request)
