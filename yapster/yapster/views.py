from django.http import HttpResponse

def index(request):
    print request.META['HTTP_AUTHORIZATION']
    return HttpResponse('coming soon...');