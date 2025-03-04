# DNS Updater for Cloudflare 🚀

This Python script automatically fetches your public IP and updates your Cloudflare DNS records every 30 minutes.

## 🌟 Features

- ✅ Fetches the current public IP address.
- ✅ Updates Cloudflare DNS records automatically.
- ✅ Runs inside Docker with `docker-compose`.
- ✅ Supports persistent logging for debugging and monitoring.
- ✅ Secure API key storage using environment variables (`.env` file).

---

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/eduardo911/cf_dns_updater.git
cd cf_dns_updater
---

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
---
### 3️⃣ Set Up Environment Variables
Create a .env file to store your Cloudflare API keys securely:
```bash
sudo nano .env
---
Inside .env, add:
```bash
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ZONE_ID=your_cloudflare_zone_id
---
Press CTRL + X, then Y, and ENTER to save.

### 4️⃣ Run the Script
```bash
python dns_updater.py
---
### 🐟 Logs
Logs are stored in dns_updater.log, which you can check using:
```bash
cat dns_updater.log
---
Sample Log Output:
```pgsql
2025-03-04 11:06:32,388 - INFO - DNS Updater started.
2025-03-04 11:06:32,606 - INFO - Current IP address: 1.2.3.4
2025-03-04 11:06:32,906 - INFO - DNS Records fetched successfully.
2025-03-04 11:06:33,104 - INFO - Successfully updated record *.example.com to IP 1.2.3.4.
2025-03-04 11:06:33,322 - INFO - Successfully updated record example.com to IP 1.2.3.4.
2025-03-04 11:06:33,609 - INFO - Successfully updated record www.example.com to IP 1.2.3.4.
---
To monitor logs in real time:
```bash
tail -f dns_updater.log
---