import subprocess
import time
import requests
import json

# Loki endpoint (update with your Loki URL)
LOKI_URL = "https://your-loki-url/loki/api/v1/push"

def run_istioctl_analyze(namespace):
    """Run the `istioctl analyze` command and capture logs."""
    try:
        result = subprocess.run(
            ["istioctl", "analyze", "-n", namespace],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except Exception as e:
        print(f"Error running istioctl analyze: {e}")
        return ""

def send_logs_to_loki(logs, namespace):
    """Send logs to Loki."""
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
                    "namespace": namespace,
                },
                "values": [[str(timestamp), line] for line in lines],
            }
        ]
    }

    # Send logs to Loki
    try:
        response = requests.post(
            LOKI_URL,
            data=json.dumps(loki_payload),
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 204:
            print(f"Failed to send logs to Loki: {response.status_code} {response.text}")
        else:
            print("Logs successfully sent to Loki.")
    except Exception as e:
        print(f"Error sending logs to Loki: {e}")

if __name__ == "__main__":
    namespace = "aks-istio-ingress"
    interval = 60  # Run every 60 seconds

    while True:
        logs = run_istioctl_analyze(namespace)
        send_logs_to_loki(logs, namespace)
        time.sleep(interval)
