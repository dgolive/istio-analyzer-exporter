import subprocess
import time
import requests
import json
import logging
import sys
import os

# Logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("App starting...")

# Loki endpoint (update with your Loki URL)


def run_istioctl_analyze():
    """Run the `istioctl analyze --all-namespaces` cmd and capture logs."""
    try:
        result = subprocess.run(
            [
                "istioctl",
                "analyze",
                "--all-namespaces",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except Exception as e:
        logger.error(f"Error running istioctl analyze: {e}")
        return ""


def send_logs_to_loki(logs):
    """Send logs to your Logging Tool."""
    if not logs.strip():
        return

    # Format logs for Loki
    timestamp = int(time.time() * 1e9)  # Nanoseconds
    lines = logs.splitlines()
    loki_payload = {
        "streams": [
            {
                "stream": {
                    "job": "istioctl-analyze",
                    "namespace": "all",
                    "cluster": CLUSTER_NAME,
                },
                "values": [[str(timestamp), line] for line in lines],
            }
        ]
    }

    # Send logs to your Logging Tool
    try:
        response = requests.post(
            LOGGING_TOOL_URL,
            data=json.dumps(loki_payload),
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 204:
            logger.error(
                f"Failed to send logs: {response.status_code} {response.text}"
            )
        else:
            logger.info("Logs successfully sent to your Logging Tool.")
    except Exception as e:
        logger.exception(f"Error sending logs to your Logging Tool: {e}")


if __name__ == "__main__":
    interval = 60
    CLUSTER_NAME = os.getenv("CLUSTER_NAME", "unknow-cluster")
    LOGGING_TOOL_URL = os.getenv("LOGGING_TOOL_URL", "unknow-cluster")

    while True:
        logs = run_istioctl_analyze()
        send_logs_to_loki(logs)
        time.sleep(interval)
