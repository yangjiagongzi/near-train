from django.http import HttpResponseRedirect
from django.urls import reverse
from .init_data import init_stations, init_trains


def update(request):
    init_stations()
    init_trains()
    return HttpResponseRedirect(reverse('plan:index'))
