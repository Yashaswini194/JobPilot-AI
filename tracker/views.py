from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .ai import analyze_job
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


def analyze_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    result = error = None
    resume = request.session.get("resume_text", "")

    if request.method == "POST":
        resume = request.POST.get("resume_text", "").strip()
        request.session["resume_text"] = resume
        if not app.job_description.strip():
            error = "This application has no job description. Click Edit and paste it first."
        elif not resume:
            error = "Please paste your resume text."
        else:
            try:
                result = analyze_job(app.job_description, resume)
            except Exception as exc:
                error = f"AI analysis failed: {exc}"

    return render(request, "tracker/analyze.html",
                  {"app": app, "result": result, "error": error, "resume": resume})
