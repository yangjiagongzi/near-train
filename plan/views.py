from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Station


def index(request):
    station_list = Station.objects.order_by('-station_no')[:10]
    context = {'station_list': station_list}
    return render(request, 'plan/index.html', context)
