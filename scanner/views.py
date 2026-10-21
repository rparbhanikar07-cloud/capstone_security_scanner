from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import ScanProfile
from .engine import VulnerabilityEngine
import threading

def index(request):
    return render(request, 'scanner/index.html')

def start_scan_api(request):
    if request.method == "POST":
        target_url = request.POST.get('target_url')
        # Assigns to authenticated user or superuser
        user = request.user if request.user.is_authenticated else None
        
        scan = ScanProfile.objects.create(user=user, target_url=target_url)
        
        engine = VulnerabilityEngine(scan)
        thread = threading.Thread(target=engine.execute_scan)
        thread.start()
        
        return JsonResponse({'scan_id': scan.id, 'status': 'started'})

def scan_status_api(request, scan_id):
    scan = get_object_or_404(ScanProfile, pk=scan_id)
    logs = list(scan.logs.values('timestamp', 'message'))
    vulns = list(scan.vulnerabilities.values('vulnerability_type', 'severity', 'endpoint', 'remediation'))
    
    return JsonResponse({
        'status': scan.status,
        'logs': logs,
        'vulnerabilities': vulns
    })
from django.http import HttpResponse

def vulnerable_testbed(request):
    # This intentionally reflects user input without sanitization (XSS vulnerability)
    user_input = request.GET.get('search', '')
    html = f"""
    <html><body>
        <h1>Search Results</h1>
        <form action="/testbed/" method="GET">
            <input type="text" name="search" placeholder="Search...">
            <button type="submit">Go</button>
        </form>
        <p>You searched for: {user_input}</p>
    </body></html>
    """
    return HttpResponse(html)