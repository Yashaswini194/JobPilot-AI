from datetime import date
from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("assessment", "Assessment"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]

    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    job_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_date = models.DateField(default=date.today)
    interview_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    job_description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    @property
    def follow_up_due(self):
        return (
            self.follow_up_date is not None
            and self.follow_up_date <= date.today()
            and self.status not in ("offer", "rejected")
        )
