from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ApplicationForm
from .models import Application


class ApplicationListView(ListView):
    model = Application
    context_object_name = "applications"

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")
        return qs.filter(status=status) if status else qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["counts"] = [
            (value, label, Application.objects.filter(status=value).count())
            for value, label in Application.STATUS_CHOICES
        ]
        return ctx


class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy("application_list")


class ApplicationUpdateView(UpdateView):
    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy("application_list")


class ApplicationDeleteView(DeleteView):
    model = Application
    success_url = reverse_lazy("application_list")
