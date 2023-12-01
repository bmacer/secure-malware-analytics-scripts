"""
This module deletes **all** of an organization's Secure Malware Analytics samples.

The two values that must be updated are:

ACCESS_TOKEN = "your-api-access-token"
Your access token (API) available in your account > API key.

ORGANIZATION_ID = "your-organization-id"
Your organization ID, which can be found the dashboard > your account > 
click on your organization name > copy the ID from the URL

Python library requirement: requests is the only required library

`python -m pip install requests`
Running the script:

`python delete-all-samples.py`
"""
import logging
import sys
import requests

# Log file name
LOG_FILE_PATH = "delete-samples.log"
# API access token
ACCESS_TOKEN = "your-api-access-token"
# Your organization ID, which can be found the dashboard > your account > click
# on your organization name > copy the ID from the URL
ORGANIZATION_ID = "your-organization-id"
# Max number of samples to delete.  Configure as desired.
MAX_DELETES = 1000

print(f"Logs will be written to {LOG_FILE_PATH}")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("")
logging.info("")
logging.info("Running delete-all-samples.py.")

if ACCESS_TOKEN == "your-api-access-token":
    print("Please update ACCESS_TOKEN with your API access token.")
    logging.error("Please update ACCESS_TOKEN with your API access token.")
    sys.exit(1)

if ORGANIZATION_ID == "your-organization-id":
    print("Please update ORGANIZATION_ID with your organization ID.")
    logging.error("Please update ORGANIZATION_ID with your organization ID.")
    sys.exit(1)

# MAX_LOOPS is to prevent accidentally running a while loop forever
MAX_LOOPS = 100
BASE_URL = "https://panacea.threatgrid.com/api/v3"
LOOP_NUMBER = 0
OFFSET = 0
TIMEOUT_SECONDS = 10

sample_ids = []
while True:
    LOOP_NUMBER += 1
    if LOOP_NUMBER > MAX_LOOPS:
        logging.error("Max loops reached. Something probably went wrong: %s", MAX_LOOPS)
        break
    samples_url = (
        f"{BASE_URL}/organizations/{ORGANIZATION_ID}/samples?OFFSET={OFFSET}&limit=500"
    )
    logging.info("Requesting samples from %s", samples_url)
    OFFSET += 500

    # Get all samples for the last 24 hours
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    response = requests.get(samples_url, headers=headers, timeout=TIMEOUT_SECONDS)

    if response.status_code != 200:
        logging.error("Failed to get samples. Error: %s", response.text)
        break

    samples = response.json()
    data = samples.get("data", {})
    items = data.get("items", [])

    if not items:
        logging.info("No more samples found.")
        break

    for item in items:
        sample_id = item.get("sample")
        if sample_id:
            sample_ids.append(sample_id)
            logging.info("Found sample ID: %s", sample_id)

logging.info("Found %s sample IDs", len(sample_ids))

DELETE_URL = f"{BASE_URL}/samples"

SUCCESSFUL_DELETES = 0
FAILED_DELETES = 0
for sample_id in sample_ids:
    if SUCCESSFUL_DELETES + FAILED_DELETES >= MAX_DELETES:
        logging.warning("Reached max deletes: %s", MAX_DELETES)
        break
    delete_sample_url = f"{DELETE_URL}/{sample_id}"
    logging.info("Deleting sample ID: %s", sample_id)
    response = requests.delete(
        delete_sample_url, headers=headers, timeout=TIMEOUT_SECONDS
    )
    if response.status_code > 200 and response.status_code < 300:
        SUCCESSFUL_DELETES += 1
        logging.info("Sample %s deleted successfully.", sample_id)

    else:
        FAILED_DELETES += 1
        logging.error(
            "Failed to delete sample %s. Error: %s URL: DELETE %s",
            sample_id,
            response.text,
            delete_sample_url,
        )

logging.info("Successfully deleted %s samples.", SUCCESSFUL_DELETES)
logging.info("Failed to delete %s samples.", FAILED_DELETES)
logging.info("Delete job is complete.")
