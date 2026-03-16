#!/var/ossec/framework/python/bin/python3

import json
import sys
import os
import re
import logging
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact

# ===== USER CONFIGURATION =====
API_KEY = "<replace_with_API_of_user_from_HIVE>"
HIVE_URL = "http://<IP_OF_THEHIVE_MACHINE>:9000"

lvl_threshold = 0
debug_enabled = False
info_enabled = True
# ==============================

pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log_file = f"{pwd}/logs/integrations.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO if info_enabled else logging.WARNING)

fh = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Initialize TheHive API
hive = TheHiveApi(HIVE_URL, API_KEY)

def flatten_json(data, prefix="", output=None):
    if output is None:
        output = []
    for key, value in data.items():
        if isinstance(value, dict):
            flatten_json(value, f"{prefix}.{key}" if prefix else key, output)
        else:
            output.append(f"{prefix}.{key}|||{value}")
    return output

def markdown_format(items):
    description = ""
    for item in items:
        key, value = item.split("|||", 1)
        description += f"**{key}** : {value}\n"
    return description

def detect_artifacts(text):
    artifacts = []

    ips = re.findall(r'\d+\.\d+\.\d+\.\d+', text)
    domains = re.findall(r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    hashes = re.findall(r'\b[a-fA-F0-9]{32,64}\b', text)

    for ip in ips:
        artifacts.append(AlertArtifact(dataType="ip", data=ip))

    for domain in domains:
        artifacts.append(AlertArtifact(dataType="domain", data=domain))

    for h in hashes:
        artifacts.append(AlertArtifact(dataType="hash", data=h))

    return artifacts

def severity_map(level):
    level = int(level)

    if level <= 5:
        return 1
    elif level <= 10:
        return 2
    else:
        return 3

def main(args):

    try:
        alert_file = args[1]

        with open(alert_file) as f:
            wazuh_alert = json.load(f)

        flattened = flatten_json(wazuh_alert)
        description = markdown_format(flattened)

        artifacts = detect_artifacts(description)

        sourceRef = str(uuid.uuid4())[:8]

        severity = severity_map(wazuh_alert["rule"]["level"])

        alert = Alert(
            title=wazuh_alert["rule"]["description"],
            tlp=2,
            severity=severity,
            tags=["wazuh", "siem"],
            description=description,
            type="wazuh_alert",
            source="wazuh",
            sourceRef=sourceRef,
            artifacts=artifacts
        )

        if int(wazuh_alert["rule"]["level"]) >= lvl_threshold:

            response = hive.create_alert(alert)

            if response.status_code == 201:
                logger.info("Alert successfully sent to TheHive")
            else:
                logger.error(f"TheHive API error: {response.text}")

    except Exception as e:
        logger.error(f"Integration error: {str(e)}")

if __name__ == "__main__":
    main(sys.argv)
