# urls for the employees app.

from django.urls import path

from .views import MultiFormCreateView

urlpatterns = [
    path("create/", MultiFormCreateView.as_view(), name="create"),
]
