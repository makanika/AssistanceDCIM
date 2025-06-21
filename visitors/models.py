from django.db import models

class VisitorLog(models.Model):
    """
    Records visits to the data centre.
    """
    visitor_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True, null=True)
    purpose = models.CharField(max_length=255)
    visit_date = models.DateField()
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.visitor_name} on {self.visit_date.strftime('%Y-%m-%d')} for {self.purpose}"

    class Meta:
        ordering = ['-visit_date', '-time_in'] # Order by latest visits

