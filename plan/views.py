from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.urls import reverse
from .models import Station
import json


def index(request):
    station_list = Station.objects.order_by('-station_no')[:10]
    context = {'station_list': station_list}
    return render(request, 'plan/index.html', context)


def search(request):
    postBody = request.body
    search_name = json.loads(postBody)['name']

    result = {}
    result['list'] = list()

    if len(search_name) != 0:
        search_list = Station.objects.filter(
            origin_info__contains=search_name).values()[0:10]
        result['list'] = list(search_list)

    print(result)
    return JsonResponse(result)
