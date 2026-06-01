from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.is_staff and not user.is_superuser:
            if user.check_password(user.email):
                if not self._is_allowed_path(request.path):
                    messages.error(
                        request,
                        "Necesitas cambiar la contraseña temporal para continuar.",
                    )
                    return redirect("perfil")
        return self.get_response(request)

    def _is_allowed_path(self, path):
        allowed_paths = {
            reverse("perfil"),
            reverse("logout"),
            reverse("login"),
        }
        if path in allowed_paths:
            return True
        if path.startswith("/password-reset/") or path.startswith("/reset/"):
            return True
        static_url = settings.STATIC_URL or ""
        if static_url:
            if not static_url.startswith("/"):
                static_url = "/" + static_url
            if path.startswith(static_url):
                return True
        if path.startswith("/admin/"):
            return True
        return False
