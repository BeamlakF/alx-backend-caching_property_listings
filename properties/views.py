from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)  # 15 minutes
def property_list(request):
    properties = Property.objects.all()
    data = list(properties.values())  # convert queryset to list of dicts
    return JsonResponse({"properties": data})  # return as JSON object

@cache_page(60 * 15)  # 15-minute view-level cache
def property_list(request):
    properties = get_all_properties()  # low-level cache for 1 hour
    data = list(properties.values())
    return JsonResponse({"properties": data})