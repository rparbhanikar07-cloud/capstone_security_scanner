document.addEventListener('DOMContentLoaded', () => {
    const scanForm = document.querySelector('#scan-form');
    const terminalOutput = document.querySelector('#terminal-log');
    const vulnContainer = document.querySelector('#vuln-results');
    let pollInterval = null;

    if (scanForm) {
        scanForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(scanForm);
            
            const response = await fetch('/api/scan/start/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            const data = await response.json();
            if (data.scan_id) {
                terminalOutput.innerHTML = "> Scan initiated... Connecting to worker engine...\n";
                pollInterval = setInterval(() => pollScanStatus(data.scan_id), 2000);
            }
        });
    }

    async function pollScanStatus(scanId) {
        const res = await fetch(`/api/scan/status/${scanId}/`);
        const data = await res.json();
        
        terminalOutput.innerHTML = data.logs.map(l => `[${l.timestamp}] ${l.message}`).join('\n');
        terminalOutput.scrollTop = terminalOutput.scrollHeight;

        if (data.vulnerabilities.length > 0) {
            vulnContainer.innerHTML = data.vulnerabilities.map(v => `
                <div class="card my-2 border-${v.severity === 'HIGH' ? 'danger' : 'warning'}">
                    <div class="card-body">
                        <h5 class="card-title">${v.vulnerability_type} <span class="badge bg-danger">${v.severity}</span></h5>
                        <p class="card-text"><strong>Endpoint:</strong> ${v.endpoint}</p>
                        <p class="card-text"><strong>Remediation:</strong> ${v.remediation}</p>
                    </div>
                </div>
            `).join('');
        }

        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
            clearInterval(pollInterval);
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});