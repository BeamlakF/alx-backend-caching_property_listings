from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties
from django.http import JsonResponse

@cache_page(60 * 15)  # 15 minutes
def property_list(request):
    properties = get_all_properties()
    data = list(properties.values())
    return JsonResponse(data, safe=False)
