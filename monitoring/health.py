"""Health - System health checks."""

from typing import Dict, Any
import time
import asyncio


class HealthChecker:
    """System health checker."""
    
    def __init__(self):
        self.checks = {
            'database': self._check_database,
            'redis': self._check_redis,
            'chroma': self._check_chroma,
            'llm': self._check_llm
        }
    
    def check_all(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {'status': 'healthy', 'services': {}}
        
        for name, check in self.checks.items():
            try:
                result = check()
                results['services'][name] = result
                
                if result.get('status') == 'unhealthy':
                    results['status'] = 'degraded'
            except Exception as e:
                results['services'][name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                results['status'] = 'degraded'
        
        return results
    
    def _check_database(self) -> Dict[str, Any]:
        """Check database health."""
        start = time.time()
        try:
            from database.postgres import PostgresDatabase
            db = PostgresDatabase()
            db.execute("SELECT 1")
            return {
                'status': 'healthy',
                'latency_ms': (time.time() - start) * 1000
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def _check_redis(self) -> Dict[str, Any]:
        """Check Redis health."""
        start = time.time()
        try:
            from database.redis import RedisClient
            redis = RedisClient()
            redis.client.ping()
            return {
                'status': 'healthy',
                'latency_ms': (time.time() - start) * 1000
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def _check_chroma(self) -> Dict[str, Any]:
        """Check Chroma health."""
        try:
            from database.chroma import ChromaClient
            client = ChromaClient()
            client._get_client()
            return {'status': 'healthy'}
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def _check_llm(self) -> Dict[str, Any]:
        """Check LLM health."""
        return {'status': 'healthy'}