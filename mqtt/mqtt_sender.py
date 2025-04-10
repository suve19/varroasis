import paho.mqtt.publish as publish
import json

msg = {
    "effected_bees": 1
}

publish.single(
    topic="varroa/camera/status",
    payload=json.dumps(msg),
    hostname="localhost",
    port=1883
)
