import requests
import psutil
from datetime import datetime, timezone
import json

# Configuration
DITTO_HOST = "http://localhost:8080"
THING_ID = "org.eclipse.ditto:camera_digitaltwin"
CREDENTIALS = ("ditto", "ditto")

def get_laptop_health():
    """Collect laptop health metrics."""
    return {
        "lastReboot": datetime.fromtimestamp(psutil.boot_time(), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "batteryPercentage": getattr(psutil.sensors_battery(), 'percent', 100),
        "cpuUsage": psutil.cpu_percent(interval=1),
        "temperature": 45.0,
        "signalStrength": -65
    }

def update_digital_twin():
    """Update the Digital Twin with complete Thing JSON."""
    # 1. Get current Thing state
    get_url = f"{DITTO_HOST}/api/2/things/{THING_ID}"
    try:
        response = requests.get(get_url, auth=CREDENTIALS)
        response.raise_for_status()
        thing_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to GET Thing: {e}")
        return

    # 2. Update only deviceHealth
    thing_data["features"]["deviceHealth"] = {
        "properties": get_laptop_health()
    }

    # 3. PUT complete Thing JSON back
    put_url = f"{DITTO_HOST}/api/2/things/{THING_ID}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.put(
            put_url,
            auth=CREDENTIALS,
            headers=headers,
            json=thing_data  # Send complete Thing JSON
        )
        response.raise_for_status()
        print(f"✅ Success! Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print("Full error response:")
            print(json.dumps(e.response.json(), indent=2))

if __name__ == "__main__":
    print("🖥️ Sending laptop health data to Digital Twin...")
    update_digital_twin()