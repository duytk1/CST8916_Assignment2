import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime
import json

def get_telemetry(location):
    return json.dumps({
        'location': location,
        'iceThickness': random.uniform(20.0, 40.0),
        'surfaceTemperature': random.uniform(-10, 30),
        'snowAccumulation': random.uniform(0, 10),
        'externalTemperature': random.uniform(-10.0, 30.0),
        'timestamp': time.time(),
    })
    
def create_client(connection_string):
    return IoTHubDeviceClient.create_from_connection_string(connection_string)
    
def send_message_azure(client, location):
    telemetry = get_telemetry()
    message = Message(str(telemetry))
    client.send_message(message)
    print(f'Sent message: {message}')
    
if __name__ == '__main__':
    print('Sending telemetry to IoT Hub...')
    client1 = create_client('HostName=iothubforassignment.azure-devices.net;DeviceId=Device1;SharedAccessKey=urkO3O+R6tYV0yWCz7wbiDujmzrN28TvY45GjKa1WL8=')
    client2 = create_client('HostName=iothubforassignment.azure-devices.net;DeviceId=Device2;SharedAccessKey=m/GFhWL4YC3TJAIkcYJxNtq/K1dXjUDJhum+cXIVIP8=')
    client3 = create_client('HostName=iothubforassignment.azure-devices.net;DeviceId=Device3;SharedAccessKey=+yNyXihxJTwwqOmjqdc9TUcyDbHkuMWqm+tOc/50hwU=')
    try:
        while True:
            client1 = create_client('HostName=iothubforassignment.azure-devices.net;DeviceId=Device1;SharedAccessKey=urkO3O+R6tYV0yWCz7wbiDujmzrN28TvY45GjKa1WL8=')
            send_message_azure(client1, 'Dow\'s Lake')
            send_message_azure(client2, 'Fifth Avenue')
            send_message_azure(client3, 'NAC')
            time.sleep(10)
    except KeyboardInterrupt:
        print('Stopped sending messages.')
    finally:
        client1.disconnect()
        client2.disconnect()
        client3.disconnect()