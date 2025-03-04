import os
import time
import datetime
import requests
import logging
from urllib.parse import urlparse  # Correct import

# Configure Logging
LOG_FILE = "/app/dns_updater.log"

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        pass  # Create an empty file

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("DNS Updater started.")

def validate_https_url(url):
    parsed_url = urlparse(url)  # Parse the URL
    if not (url.startswith("https://") and parsed_url.scheme == "https"):
        raise ValueError("The URL must use an encrypted protocol (HTTPS).")

def get_all_dns_records():
    CLOUD_API_TOKEN_ERROR = "Cloudflare API token not set in environment variables."
    CLOUD_ZONE_ID_ERROR = "Cloudflare Zone ID not set in environment variables."

    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    if not api_token:
        raise ValueError(CLOUD_API_TOKEN_ERROR)

    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    if not zone_id:
        raise ValueError(CLOUD_ZONE_ID_ERROR)

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    validate_https_url(url)

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch DNS records: {response.status_code} - {response.text}")

    logging.info("DNS Records fetched successfully.")
    return response.json()

def get_current_ip():
    url = "https://cloudflare.com/cdn-cgi/trace/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        for line in response.text.splitlines():
            if line.startswith("ip="):
                ip_address = line.split("=")[1]
                logging.info(f"Current IP address: {ip_address}")
                return ip_address
        raise ValueError("IP address not found in response")
    except Exception as e:
        logging.error(f"Failed to fetch current IP address: {e}")
        raise

def update_dns_records(records, ip_address):
    CLOUD_API_TOKEN_ERROR = "Cloudflare API token not set in environment variables."
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    if not api_token:
        raise ValueError(CLOUD_API_TOKEN_ERROR)

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    for record in records.get('result', []):
        if record['type'] in ('A', 'AAAA'):
            record_id = record['id']
            record_name = record['name']
            update_url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('CLOUDFLARE_ZONE_ID')}/dns_records/{record_id}"

            data = {
                "type": record['type'],
                "name": record_name,
                "content": ip_address,
                "ttl": record['ttl'],
                "proxied": record['proxied']
            }

            response = requests.put(update_url, headers=headers, json=data)
            if response.status_code != 200:
                logging.error(f"Failed to update record {record_name}: {response.status_code} - {response.text}")
            else:
                logging.info(f"Successfully updated record {record_name} to IP {ip_address}.")

def run_loop_for_30_days():
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(days=30)

    while datetime.datetime.now() < end_time:
        try:
            ip_address = get_current_ip()
            records = get_all_dns_records()
            update_dns_records(records, ip_address)  # Call the function to update records
        except Exception as error:
            logging.error(f"Error during execution: {error}")

        # Countdown timer for 30 minutes (displaying every 30 seconds)
        for i in range(30 * 60, 0, -30):
            print(f"Next update in {i // 60} minutes {i % 60} seconds...", end="\r")
            time.sleep(30)  # Sleep for 30 seconds
        print("")  # Clear the timer display


if __name__ == "__main__":
    while True:
        run_loop_for_30_days()

        while True:  # Keep asking until valid input is received
            user_input = input("The 30-day loop has completed. Do you want to restart? (yes/no): ").strip().lower()

            if user_input == 'no':
                logging.info("User chose to exit. Stopping the loop.")
                print("Exiting the loop.")
                break  # Break inner loop

            elif user_input == 'yes':
                logging.info("User chose to restart the loop.")
                break  # Restart 30-day loop

            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                logging.warning("Invalid input received.")

        if user_input == 'no':  # Break outer loop and exit program
            break
