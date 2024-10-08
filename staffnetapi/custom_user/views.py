from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("employees-list")
        return super().dispatch(request, *args, **kwargs)
