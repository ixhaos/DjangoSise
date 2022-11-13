from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.path_info == "/Login.html":
            return
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect("/Login.html")
