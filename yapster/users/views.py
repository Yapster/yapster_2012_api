# coding=utf-8
from django.http import HttpResponse

def index(request):
    print request.META.get('HTTP_AUTHORIZATION', '')
    return HttpResponse('coming soon...');