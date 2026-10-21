from django.contrib import admin
from .models import ScanProfile, DiscoveredEndpoint, VulnerabilityResult, ScanLog

@admin.register(ScanProfile)
class ScanProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_url', 'status', 'created_at')

@admin.register(DiscoveredEndpoint)
class DiscoveredEndpointAdmin(admin.ModelAdmin):
    list_display = ('scan', 'url', 'http_method')

@admin.register(VulnerabilityResult)
class VulnerabilityResultAdmin(admin.ModelAdmin):
    list_display = ('scan', 'vulnerability_type', 'severity', 'endpoint')

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ('scan', 'timestamp', 'message')