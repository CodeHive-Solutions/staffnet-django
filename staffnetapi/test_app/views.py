from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import FormOne, FormTwo, UserProjectFormSet
from .models import Project, User, UserProject


class MultiFormCreateView(CreateView):
    model = User  # This will be used for the first model (User)
    template_name = "multi.html"
    success_url = (
        "/success/"  # Redirect to success page after successful form submission
    )
    form_class = FormOne  # This will be used for the first form (User)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form_one = FormOne(request.POST)
        form_two = FormTwo(request.POST)
        formset = UserProjectFormSet(request.POST)

        if form_one.is_valid() and form_two.is_valid() and formset.is_valid():
            user = form_one.save()
            form_two.instance = user
            form_two.save()

            for form in formset:
                user_project = form.save(commit=False)
                user_project.user = user
                user_project.save()

            return redirect(self.success_url)

        return self.render_to_response(
            self.get_context_data(form_one=form_one, form_two=form_two, formset=formset)
        )
