🛡️ Aegis Scanner

Professional Automated Web Security Scanner

Aegis Scanner is a modular, professional-grade web application security scanner that automates reconnaissance, attack surface discovery, and SQL Injection detection using a unified injection engine.

It is designed to reflect real-world penetration testing workflows, not toy scripts.

⸻

🚀 Features

🔍 Reconnaissance
	•	Open port scanning
	•	Service fingerprinting (HTTP/HTTPS detection)
	•	Automatic web target identification
	•	Controlled scanning mode (safe by default)

🌐 Web Discovery
	•	Recursive crawling across discovered services
	•	URL normalization and deduplication
	•	Parameterized URL generation
	•	HTML form extraction (GET + POST)

🎯 Injection Point Engine
	•	Unified handling of:
	•	GET parameters
	•	POST parameters
	•	HTML form fields
	•	InjectionPoint abstraction (professional design)

💉 SQL Injection Detection

Supports multiple SQLi techniques in a single pipeline:
	•	Numeric SQL Injection
	•	String-based SQL Injection
	•	Single quote (')
	•	Double quote (")
	•	Boolean-based SQLi
	•	Error-based SQLi
	•	GET-based SQLi
	•	POST-based SQLi
	•	Form-driven SQLi

🧠 Context-Aware Engine
	•	Baseline response comparison
	•	Length-based differential analysis
	•	SQL error fingerprinting
	•	Confidence scoring

📊 Output
	•	Clear terminal reporting
	•	Confidence level per finding
	•	Technique identification
	•	Parameter-level vulnerability mapping

⸻

🏗️ Project Architecture

Aegis-Scanner/
│
├── main.py                     # Entry point
│
├── core/
│   ├── target.py               # Target abstraction
│   ├── environment.py          # WAF / environment detection
│   ├── context.py              # Shared scan context
│   ├── requester.py            # Central HTTP requester
│   └── injection_point.py      # InjectionPoint model
│
├── recon/
│   ├── port_scanner.py
│   ├── crawler.py
│   └── service_fingerprint.py
│
├── analysis/
│   ├── attack_surface.py
│   ├── forms.py
│   ├── parameters.py
│   └── injection_factory.py
│
├── attacks/
│   └── sqli_engine.py           # Unified SQLi engine
│
└── requirements.txt





⸻

🧪 How It Works (High Level)
	1.	Reconnaissance
	•	Scan ports
	•	Identify live web services
	2.	Discovery
	•	Crawl websites
	•	Extract URLs, parameters, and forms
	3.	Injection Modeling
	•	Convert URLs + forms into InjectionPoints
	4.	Unified SQLi Engine
	•	Apply numeric + string payloads
	•	Compare responses
	•	Detect errors and behavioral differences
	5.	Reporting
	•	High-confidence findings only
	•	Minimal false positives

⸻

🛠️ Installation

Requirements
	•	Python 3.9+
	•	Linux / macOS recommended
----------------------------------------------------------
Setup:

git clone https://github.com/vishalxdogra/Aegis-Scanner.git
cd Aegis-Scanner

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt


▶️ Usage
python main.py


⸻

⚠️ Legal Disclaimer

This tool is for educational and authorized security testing only.

Do NOT scan:
	•	Websites you do not own
	•	Systems without explicit permission

The author is not responsible for misuse or damage caused by this tool.

⸻

🎯 Project Goals
	•	Professional security tool architecture
	•	Minimal false positives
	•	Extensible attack engine
	•	Resume & portfolio ready
	•	Industry-aligned penetration testing logic

⸻

🧩 Future Enhancements
	•	Time-based SQLi
	•	UNION-based SQLi
	•	Authenticated scanning
	•	Session handling
	•	JSON / HTML reports
	•	GUI / Web dashboard
	•	Plugin-based attack modules



⭐ Support

If you found this project useful:
	•	⭐ Star the repository
	•	🛠️ Fork and extend
	•	📩 Open issues for improvements
