from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.cache import patch_cache_control


class ReadOnlyDemoMiddleware:
    """Default deny: only explicitly approved read views and login/logout run."""
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not settings.READ_ONLY_DEMO:
            return None
        name = request.resolver_match.url_name
        authentication = name in {"login", "logout"} and view_func.__module__ == "login.views"
        readable = getattr(view_func, "demo_readable", False)
        if not authentication and (not readable or request.method not in {"GET", "HEAD", "OPTIONS"}):
            return HttpResponseForbidden("Demonstração somente leitura: alterações desativadas.")

    def __call__(self, request):
        response = self.get_response(request)
        if settings.READ_ONLY_DEMO:
            patch_cache_control(response, private=True, no_store=True)
        return response
