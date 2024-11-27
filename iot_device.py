import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

CONNECTION_STRING = "Your IoT Hub device connection string here"

def get_telemetry():
    return {
        "location": "Dow's Lake",
        "iceThickness": random.uniform(20.0, 40.0),
        "surfaceTemperature": random.uniform(-10, 30.0),
        "snowAccumulation": random.uniform(0.0, 10.0),
        "externalTemperature": random.uniform(-10.0, 30.0),
        "timestamp": time.time(),
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()