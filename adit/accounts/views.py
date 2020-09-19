from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .forms import RegistrationForm
from .models import User


class UserProfileView(LoginRequiredMixin, AccessMixin, DetailView):
    model = User
    template_name = "accounts/user_profile.html"

    def dispatch(self, request, *args, **kwargs):
        """Only superuser, staff and the user himself has access."""
        check_access = True
        if request.user.is_superuser or request.user.is_staff:
            check_access = False

        if check_access and request.user.pk != kwargs["pk"]:
            self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "accounts/registration.html"

    def form_valid(self, form):
        form.instance.is_active = False
        return super().form_valid(form)