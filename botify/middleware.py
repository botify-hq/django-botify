from django.utils.functional import SimpleLazyObject

from . import Botify

def get_botify(request):
    if not hasattr(request, '_cached_botify'):
        request._cached_botify = Botify(request.META)
    return request._cached_botify

class BotifyMiddleware(object):

    def process_request(self, request):
        request.botify = SimpleLazyObject(lambda: get_botify(request))

    def process_response(self, request, response):
        if Botify.is_crawlable(request.META.get('HTTP_REFERER', None),
                                     request.META.get('HTTP_USER_AGENT', None)) \
           and hasattr(request, 'botify'):
            request.botify.set_code(response.status_code)
            request.botify.record()
        return response

