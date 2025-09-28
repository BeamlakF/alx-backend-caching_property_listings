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
    conn = get_redis_connection("default")
    info = conn.info('stats')
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    ratio = hits / (hits + misses) if (hits + misses) > 0 else 0
    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": ratio
    }
    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics

def get_all_properties():
    # Try to fetch from Redis cache
    properties = cache.get('all_properties')
    if properties is not None:
        return properties  # cache hit

    # Cache miss → fetch from database
    properties = Property.objects.all()
    cache.set('all_properties', properties, 3600)  # store in Redis for 1 hour
    return properties