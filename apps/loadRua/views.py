from django.shortcuts import render
from django.shortcuts import HttpResponse
from .tasks import main

main()

# Create your views here.
def index(request):
    pass
    return HttpResponse(request, "demo")
