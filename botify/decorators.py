def set_tracker(trackers):
    def wrap(f):
        def _f(request, *args, **kwargs):
            if hasattr(request, 'botify'):
                request.botify.add_tracker(trackers)
            return f(request, *args, **kwargs)
        return _f
    return wrap

def set_canonical(canonical):
    def wrap(f):
        def _f(request, *args, **kwargs):
            if hasattr(request, 'botify'):
                request.botify.set_canonical(canonical)
            return f(request, *args, **kwargs)
        return _f
    return wrap

