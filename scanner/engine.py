import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import DiscoveredEndpoint, VulnerabilityResult, ScanLog

class VulnerabilityEngine:
    def __init__(self, scan_profile):
        self.scan = scan_profile
        self.target_url = scan_profile.target_url

    def log(self, message):
        ScanLog.objects.create(scan=self.scan, message=message)

    def crawl_dom(self):
        self.log(f"Starting DOM crawl on {self.target_url}")
        try:
            response = requests.get(self.target_url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = soup.find_all('form')
            for form in forms:
                action = form.get('action')
                target_endpoint = urljoin(self.target_url, action) if action else self.target_url
                inputs = [input_tag.get('name') for input_tag in form.find_all('input') if input_tag.get('name')]
                
                DiscoveredEndpoint.objects.create(
                    scan=self.scan,
                    url=target_endpoint,
                    http_method=form.get('method', 'GET').upper(),
                    form_inputs=inputs
                )
            self.log(f"DOM Crawl finished. Found {len(forms)} form endpoints.")
        except Exception as e:
            self.log(f"Crawl error: {str(e)}")

    def test_xss_heuristics(self, endpoint, param):
        payload = "<script>alert('CS50W_XSS')</script>"
        params = {param: payload}
        try:
            res = requests.get(endpoint.url, params=params, timeout=5)
            if payload in res.text:
                VulnerabilityResult.objects.create(
                    scan=self.scan,
                    vulnerability_type="Reflected XSS",
                    severity="HIGH",
                    endpoint=endpoint.url,
                    parameter=param,
                    payload_used=payload,
                    remediation="Sanitize user inputs and use Context-Aware HTML Encoding or Content Security Policy (CSP)."
                )
                self.log(f"VULNERABILITY FOUND: Reflected XSS on parameter '{param}'")
        except Exception as e:
            self.log(f"Execution error testing XSS: {str(e)}")

    def execute_scan(self):
        self.scan.status = 'RUNNING'
        self.scan.save()
        self.crawl_dom()
        
        for endpoint in self.scan.endpoints.all():
            for param in endpoint.form_inputs:
                self.test_xss_heuristics(endpoint, param)
                
        self.scan.status = 'COMPLETED'
        self.scan.save()
        self.log("Scan process completed successfully.")