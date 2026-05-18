# Network Vulnerability Checker Tool v1.0

A lightweight, multi-threaded command-line utility written in Python to perform network reconnaissance, service banner grabbing, and basic vulnerability analysis against local or remote hosts.

## 🚀 Features

*   **Multi-threaded Port Scanner:** Concurrently scans ranges or individual lists of TCP ports using a thread pool for maximum efficiency.
*   **Service Banner Grabber:** Interrogates open ports to extract service version strings (including automated HTTP HEAD injections for web services).
*   **Vulnerability Auditor:** Cross-references captured service banners against a built-in signature database to highlight potential CVE vulnerabilities.
  


## 🛠️ Installation

1. **Clone the Repository:**
   ```bash
 git clone [https://github.com/mobatatare09/network-vulnerability-checker.git](https://github.com/mobatatare09/network-vulnerability-checker.git)
   cd network-vulnerability-checker
   
  ## 📖 Usage Instructions

Run the script from your terminal or command prompt:

bash
python main.py

## ⚠️ Disclaimer
This tool is designed purely for educational purposes and authorized network security testing. Do not execute scanning or vulnerability verification checks against target systems without explicit prior permission from the system owner. Unauthorised scanning can be interpreted as a malicious network indicator.
