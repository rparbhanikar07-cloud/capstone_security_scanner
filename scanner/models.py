from django.db import models
from django.contrib.auth.models import User

class ScanProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scans",null=True,blank=True)
    target_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return f"{self.target_url} - {self.status}"

class DiscoveredEndpoint(models.Model):
    scan = models.ForeignKey(ScanProfile, on_delete=models.CASCADE, related_name="endpoints")
    url = models.URLField()
    http_method = models.CharField(max_length=10, default="GET")
    form_inputs = models.JSONField(default=list)

class VulnerabilityResult(models.Model):
    SEVERITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
        ('INFO', 'Info'),
    ]
    scan = models.ForeignKey(ScanProfile, on_delete=models.CASCADE, related_name="vulnerabilities")
    vulnerability_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    endpoint = models.URLField()
    parameter = models.CharField(max_length=100, blank=True, null=True)
    payload_used = models.TextField(blank=True, null=True)
    remediation = models.TextField()

class ScanLog(models.Model):
    scan = models.ForeignKey(ScanProfile, on_delete=models.CASCADE, related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()