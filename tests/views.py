from django.http import HttpResponse

from botify.decorators import set_canonical, set_tracker


def simple(request):
    return HttpResponse('Ok')


@set_canonical('canonical')
def canonical(request):
    return HttpResponse('Ok')


@set_tracker('tracker')
def tracker(request):
    return HttpResponse('Ok')
