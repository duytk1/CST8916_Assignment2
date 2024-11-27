import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime
import json

CONNECTION_STRING = 'HostName=iothubforassignment.azure-devices.net;DeviceId=Device1;SharedAccessKey=urkO3O+R6tYV0yWCz7wbiDujmzrN28TvY45GjKa1WL8='

def get_telemetry():
    list_sensors = []
    list_sensors.append({"Device1": get_sensor('Ottawa')})
    list_sensors.append({"Device2": get_sensor('Toronto')})
    list_sensors.append({"Device3": get_sensor('Missisauga')})
    return json.dumps(list_sensors)
    
    
def get_sensor(location):
    return {
        'location': location,
        'iceThickness': random.uniform(20.0, 40.0),
        'surfaceTemperature': random.uniform(-10, 30),
        'snowAccumulation': random.uniform(0, 10),
        'externalTemperature': random.uniform(-10.0, 30.0),
        'timestamp': time.time(),
    }
    
if __name__ == '__main__':
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print('Sending telemetry to IoT Hub...')
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f'Sent message: {message}')
            time.sleep(10)
    except KeyboardInterrupt:
        print('Stopped sending messages.')
    finally:
        client.disconnect()