# Automated Web Application Penetration Testing & Vulnerability Assessment Dashboard

#### CS50’s Web Programming with Python and JavaScript - Capstone Final Project

---

## Distinctiveness and Complexity

### Distinctiveness
The Automated Web Application Penetration Testing & Vulnerability Assessment Dashboard is a specialized, interactive security testing platform built to automate web application vulnerability discovery. When evaluating the distinctiveness of this project relative to the core curriculum of CS50’s Web Programming with Python and JavaScript, it is immediately apparent that this application operates in a completely distinct domain—cybersecurity, network diagnostics, and automated software assessment.

Unlike traditional web projects built throughout the course—such as Google Search clones (Project 0), Wikipedia-style encyclopedias (Project 1), e-commerce auction sites (Project 2), email clients (Project 3), or Twitter-like social networking platforms (Project 4)—this capstone project is neither a CRUD-heavy content management site nor a social media or commerce platform. It explicitly avoids standard e-commerce patterns (listings, bids, comments, watchlists) and social network constructs (user feeds, posts, follows, likes). Instead, it serves as an administrative security workstation where security analysts and developers can execute real-time payload injection tests, inspect HTTP response structures, parse Document Object Model (DOM) form vectors, and evaluate web security postures.

### Complexity
The architectural complexity of this application spans both the asynchronous backend execution pipeline and the interactive client-side rendering layer. The core technical challenges solved in this project include:

1. **Asynchronous Background Processing with Threading:** Standard web applications process HTTP requests synchronously, blocking the thread until a response is returned. Security scanning, by nature, involves crawling multiple links, parsing HTML structures, sending crafted HTTP payloads, and waiting for server responses. Running these operations synchronously inside a Django view would cause HTTP timeouts and freeze the user interface. To solve this, the application implements an asynchronous worker architecture in `scanner/engine.py`. When a user initiates a scan, Django spawns a background `threading.Thread` instance that executes the engine independently of the web server's primary request-response loop.

2. **Custom Web Crawling and DOM Vector Extraction:** The scanning engine utilizes `BeautifulSoup` and `requests` to perform automated reconnaissance on target URLs. It programmatically fetches HTML documents, parses the DOM tree to isolate `<form>` elements and input controls (`<input>`, `<textarea>`, `<select>`), extracts action attributes and HTTP methods (GET/POST), and constructs input parameter maps. This DOM vector extraction forms the foundation for automated security testing.

3. **Context-Aware Payload Injection & Heuristic Verification:** Once vectors are identified, the engine executes payload injection heuristics to test for vulnerabilities such as Reflected Cross-Site Scripting (XSS). The engine crafts targeted test strings containing unique boundary markers and executable script signatures, dispatches HTTP requests to the target endpoints, and analyzes the reflected response body. If the payload is rendered verbatim without proper HTML entity encoding or sanitization context, the heuristic flags the vulnerability, assigns a severity rating (High/Medium/Low), and generates actionable remediation advice.

4. **Real-Time Terminal Streaming via Asynchronous Frontend Polling:** To provide a dynamic terminal interface similar to professional command-line security tools (such as Nmap or OWASP ZAP), the application implements a decoupled logging pipeline. As the backend scanning engine runs, it writes micro-logs and milestone timestamps into the `ScanLog` database model. On the frontend, client-side JavaScript (`app.js`) initiates an asynchronous HTTP polling loop (`fetch` API) every second to retrieve unread logs, dynamically streaming console messages into a custom terminal container with smooth auto-scrolling behavior.

5. **Relational Data Modeling & Admin Integration:** The application schema links target profiles, discovered endpoints, vulnerability findings, and live logs using Django’s Object-Relational Mapper (ORM) with relational Foreign Key constraints, cascading rules, and customized Django Admin management interfaces.

---

## Project Structure & File Inventory

Below is a detailed inventory describing the purpose and contents of every file created within the repository: 
`````capstone_security_scanner/
│
├── config/                          # Main Django Project Configuration Package
│   ├── init.py                  # Package initialization file
│   ├── settings.py                  # Global Django settings, INSTALLED_APPS, middleware, and database setup
│   ├── urls.py                      # Root URL routing, including admin/ and app inclusion
│   ├── asgi.py                      # Asynchronous Server Gateway Interface entry point
│   └── wsgi.py                      # Web Server Gateway Interface entry point
│
├── scanner/                         # Core Application Package
│   ├── init.py                  # App package initialization file
│   ├── admin.py                     # Customized Django Admin site registration for models
│   ├── apps.py                      # Application configuration class (ScannerConfig)
│   ├── engine.py                    # Asynchronous security scanning engine & payload heuristics
│   ├── models.py                    # Database schema (ScanProfile, DiscoveredEndpoint, VulnerabilityResult, ScanLog)
│   ├── tests.py                     # Automated Django unit tests for models and view endpoints
│   ├── urls.py                      # App-specific URL routing rules
│   └── views.py                     # HTTP request handlers, async thread starters, and JSON API endpoints
│
├── templates/
│   └── scanner/
│       └── index.html               # Main dashboard HTML template with terminal UI and result cards
│
├── static/
│   └── scanner/
│       ├── app.js                   # JavaScript logic for form handling, AJAX polling, and UI updates
│       └── style.css                # Custom CSS styling for terminal emulation and severity badges
│
├── db.sqlite3                       # SQLite database storing scan profiles, logs, and findings
├── manage.py                        # Django command-line execution utility
└── requirements.txt                 # Python package dependency manifest````

### Detailed File Descriptions

* **`scanner/engine.py`**: Contains the core Python security engine logic. Defines the `SecurityScanner` class which handles HTML parsing, form parameter extraction, HTTP payload injection, Reflected XSS detection heuristics, and safe thread management.
* **`scanner/models.py`**: Defines four key database models:
  * `ScanProfile`: Tracks the target URL, creation timestamp, overall scan status (PENDING, RUNNING, COMPLETED, FAILED), and total vulnerabilities found.
  * `DiscoveredEndpoint`: Stores endpoints discovered during crawling, including URL path and HTTP method.
  * `VulnerabilityResult`: Logs specific findings, including vulnerability type, severity rating (HIGH, MEDIUM, LOW), target endpoint, payload used, and remediation recommendations.
  * `ScanLog`: Records real-time execution messages linked to a scan profile for terminal output streaming.
* **`scanner/views.py`**: Handles incoming browser requests. Contains `index` (renders main UI), `start_scan` (validates URL input and launches the background engine thread), `get_scan_logs` (returns JSON log updates for frontend polling), and `get_scan_results` (returns JSON vulnerability results).
* **`scanner/admin.py`**: Registers models with custom `list_display` fields in Django Admin to allow administrative monitoring of scan history and findings.
* **`templates/scanner/index.html`**: The single-page dashboard interface structured with modern Bootstrap 5 components, featuring a target URL input box, progress indicators, a dark terminal console window, and color-coded vulnerability alert cards.
* **`static/scanner/app.js`**: Pure JavaScript (ES6) controlling client-side interactivity. Manages form submissions, initiates recurring `fetch()` API calls to poll log endpoints, appends log lines to the terminal DOM element in real-time, and renders result cards upon scan completion.
* **`static/scanner/style.css`**: CSS stylesheet providing terminal aesthetics (monospace font styling, scrollbar behaviors, neon text accenting) and custom responsive grid styling.
* **`requirements.txt`**: Specifies all required Python libraries (`Django`, `requests`, `beautifulsoup4`).

---

## How to Run the Application

Follow these step-by-step instructions to set up and run the application locally:

### 1. Prerequisites
Ensure you have Python 3.10+ and `pip` installed on your system.

### 2. Clone the Repository & Navigate to Directory
```bash
git clone https://github.com/rparbhanikar07-cloud/capstone_security_scanner.git
cd capstone_security_scanner

###3. Install Python Dependencies
Install all required third-party libraries listed in requirements.txt:

Bash:
pip install -r requirements.txt

###4. Run Database Migrations
Initialize your local SQLite database schema:

Bash:
python manage.py makemigrations
python manage.py migrate

###5. Create a Django Superuser (Optional for Admin Access)
Create an administrative account to access the backend Django Admin dashboard:

Bash
python manage.py createsuperuser
(Follow the terminal prompts to set a username and password)

###6. Start the Development Server
Launch the local Django server:

Bash
python manage.py runserver

###7. Access the Application in Your Browser
Main Security Dashboard: Open http://127.0.0.1:8000/

Django Admin Management Console: Open http://127.0.0.1:8000/admin/

###Additional Notes for Course Staff
Simulated Testbed: The application includes a built-in testbed endpoint(http://127.0.0.1:8000/testbed/) designed specifically to simulate a vulnerable Reflected XSS form vector. This allows safe, controlled verification of the engine's payload injection heuristics without requesting external network resources.

Asynchronous Timing: Because scans are executed in background threads, there is a brief multi-second execution window between clicking "Launch Assessment" and receiving the final vulnerability summary card. The live terminal window streams progress logs during this period.

Mobile Responsiveness: The dashboard UI is built with flexible Bootstrap grid components, ensuring mobile responsiveness across desktop, tablet, and smartphone viewports.