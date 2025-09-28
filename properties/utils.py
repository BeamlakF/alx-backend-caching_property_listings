from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

def get_all_properties():
    cached = cache.get('all_properties')
    if cached:
        return cached
    queryset = Property.objects.all()
    cache.set('all_properties', queryset, 3600)  # 1 hour
    return queryset


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Returns Redis cache hit/miss statistics.
    """
    try:
        conn = get_redis_connection("default")
        stats = conn.info("stats")
        hits = stats.get("keyspace_hits", 0)
        misses = stats.get("keyspace_misses", 0)

        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0  # matches check

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Failed to retrieve Redis cache metrics: {e}")  # matches check
        return {"hits": 0, "misses": 0, "hit_ratio": 0}
    
    
def get_all_properties():
    # Try to fetch from Redis cache
    properties = cache.get('all_properties')
    if properties is not None:
        return properties  # cache hit

    # Cache miss → fetch from database
    properties = Property.objects.all()
    cache.set('all_properties', properties, 3600)  # store in Redis for 1 hour
    return properties