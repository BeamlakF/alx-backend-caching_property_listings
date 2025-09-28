from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

@cache_page(60 * 15)  # 15 minutes
def property_list(request):
    properties = Property.objects.all()
    data = list(properties.values())  # convert queryset to list of dicts
    return JsonResponse({"properties": data})  # return as JSON object
