from django.http import HttpResponsePermanentRedirect

from django.conf import settings


class AdminRedirectMiddleware:

    IGNORE_HOSTS = ["admin.schoolies.in", "127.0.0.1", "localhost"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        host = request.get_host()
        print("admin middleware intercepting url")

        if not settings.DEBUG:

            if any(host == ignore_host for ignore_host in self.IGNORE_HOSTS):
                return response

            # Check if 'admin' is not in the host and we're not dealing with a local server
            if not host.startswith("admin."):

                print("changing the host to admin.")

                new_url = f"https://admin.{host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(new_url)
        return response
