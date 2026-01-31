🛡️ Aegis Scanner

Automated Web Application Security Scanner
Reconnaissance • Attack Surface Discovery • SQL Injection Detection

Aegis Scanner is a modular, professional-grade web security scanner designed to automate real-world penetration testing workflows.
It focuses on accurate attack surface mapping and reliable SQL Injection detection using a unified and extensible engine.

This project is built with clean architecture, low false positives, and future exploitability in mind.
It is not a toy script. It reflects how modern security tools are structured internally.

⸻

🚀 Features

🔍 Reconnaissance
	•	Open port scanning
	•	Web service identification (HTTP / HTTPS)
	•	Automatic web target detection
	•	Safe, controlled scanning by default

🌐 Web Discovery
	•	Recursive crawling
	•	URL normalization and deduplication
	•	Parameter discovery
	•	HTML form extraction
	•	GET forms
	•	POST forms

🎯 Injection Point Engine
	•	Unified InjectionPoint abstraction
	•	Supports:
	•	GET parameters
	•	POST parameters
	•	HTML form fields
	•	Centralized handling for all attack modules

💉 SQL Injection Detection

Single engine supporting multiple SQLi techniques:
	•	Numeric SQL Injection
	•	String-based SQL Injection
	•	Single quote (') injections
	•	Double quote (") injections
	•	Boolean-based SQL Injection
	•	Error-based SQL Injection
	•	GET-based SQL Injection
	•	POST-based SQL Injection
	•	Form-driven SQL Injection

🧠 Context-Aware Detection
	•	Baseline response comparison
	•	Length-based differential analysis
	•	SQL error fingerprinting
	•	Confidence scoring to reduce false positives

📊 Reporting
	•	Clear terminal output
	•	Parameter-level vulnerability mapping
	•	Technique identification
	•	Confidence level per finding
🧪 How It Works (High Level)
	1.	Reconnaissance
	•	Scan open ports
	•	Identify live web services
	2.	Discovery
	•	Crawl discovered websites
	•	Extract URLs, parameters, and forms
	3.	Injection Modeling
	•	Convert URLs and forms into InjectionPoints
	4.	SQL Injection Engine
	•	Apply numeric and string payloads
	•	Compare baseline vs injected responses
	•	Detect behavioral and error-based differences
	5.	Reporting
	•	Only high-confidence findings are reported
	•	Reduced noise and false positives

⸻

▶️ Usage

Requirements
	•	Python 3.9+
	•	Linux / macOS recommended

Setup-

git clone https://github.com/vishalxdogra/Aegis-Scanner.git
cd Aegis-Scanner

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

Run the Scanner
python main.py

You will be prompted to:
	•	Enter a target URL
	•	Choose authenticated or unauthenticated scanning

🧪 Tested Against

This project has been tested against:
	•	DVWA (local)
	•	SQLi Labs (Less-* series)
	•	testphp.vulnweb.com
	•	Custom vulnerable PHP applications
	•	Controlled lab environments

⸻

⚠️ Legal Disclaimer

This tool is strictly for educational and authorized security testing only.

❌ Do NOT scan:
	•	Websites you do not own
	•	Systems without explicit permission

The author is not responsible for misuse or damage caused by this tool.

⸻

🎯 Project Goals
	•	Professional security tool architecture
	•	Minimal false positives
	•	Extensible attack engine
	•	Industry-aligned penetration testing logic

⸻

🔮 Roadmap / Future Work
	•	Time-based SQL Injection
	•	UNION-based SQL Injection exploitation
	•	Authenticated scanning
	•	Session and cookie handling
	•	JSON / HTML reporting
	•	Exploitation modules
	•	Plugin-based attack architecture
	•	Web or GUI dashboard

⸻

⭐ Author

Vishal Dogra
