# Real-time Monitoring System for Rideau Canal Skateway
## Scenario Description

The Rideau Canal Skateway, a historic and world-renowned attraction in Ottawa, needs constant monitoring to ensure skater safety. In this project, we will help the National Capital Commission (NCC) to build a real-time data streaming system that will:

* Simulate IoT sensors to monitor ice conditions and weather factors along the canal.
* Process incoming sensor data to detect unsafe conditions in real time.
* Store the results in Azure Blob Storage for further analysis.

## System Architecture

![alt text](<Diagram.drawio (1).png>)

The Rideau Canal Skateway monitoring system consists of simulated IoT sensors at key locations (Dow’s Lake, Fifth Avenue, NAC) that generate data every 10 seconds, measuring ice thickness, surface temperature, snow accumulation, and external temperature. This data is sent to Azure IoT Hub, which manages and securely streams it to Azure Stream Analytics. Stream Analytics processes the data in real time, aggregating metrics like average ice thickness and maximum snow accumulation over 5-minute windows. The processed results are then stored in Azure Blob Storage for further analysis, enabling timely monitoring and ensuring skater safety.

## Step 1: Azure set up
First, we create a resource group:

![alt text](screenshots/resourcegroup.png)
![alt text](screenshots/resourcegroup2.png)

Second of all, we create an IoThub:

![alt text](screenshots/IoTHub1.png) ![alt text](screenshots/IoTHub2.png) ![alt text](screenshots/IoTHub3.png) ![alt text](screenshots/IoTHub4.png)

Thirdly, we create the IoTHub devices:

![alt text](screenshots/IoTHub_device1_constring1.png) ![alt text](screenshots/IoTHub_device1.png) ![alt text](screenshots/IoTHub_device2_.png) ![alt text](screenshots/IoTHub_device2_constring2.png) ![alt text](screenshots/IoTHub_device2.png) ![alt text](screenshots/IoTHub_device3_constring3.png) ![alt text](screenshots/IoTHub_device3.png)

After that, we create the storage account:

![alt text](screenshots/storageacc1.png) ![alt text](screenshots/storageacc2.png) ![alt text](screenshots/storageacc3.png)

We also create a storage container for our results:

![alt text](screenshots/storageacc_container.png) ![alt text](screenshots/storageacc_container2.png) ![alt text](screenshots/storageacc_container3.png)


Here we set up Azure Stream Analytics:

![alt text](screenshots/streamanalytics1.png) ![alt text](screenshots/streamanalytics2.png) ![alt text](screenshots/streamanalytics3.png) ![alt text](screenshots/streamanalytics4.png)

## Step 2: Write the simulation Python Scripts and queries for Azure stream analytics

On premise, we prepare a python script for Azure

``` py
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime
import json

def get_telemetry(location):
    return {
        'location': location,
        'iceThickness': random.uniform(20.0, 40.0),
        'surfaceTemperature': random.uniform(-10, 30),
        'snowAccumulation': random.uniform(0, 10),
        'externalTemperature': random.uniform(-10.0, 30.0),
        'timestamp': time.time(),
    }
    
def create_client(connection_string):
    return IoTHubDeviceClient.create_from_connection_string(connection_string)
    
def send_message_azure(client, location):
    telemetry = get_telemetry(location)
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
```
How to run the python scripts:

We install the needed packages to run the script. The most important library to run this script is IoTHubDeviceClient:

``` pip install -r requirements.txt ```

After that, since we have the connection string, the script will run and produce the sensor similation code for the IoT sensor.

Here is our queries for our stream analytics 


## Step 3: Connect Azure Stream Analytics
In the Azure Portal, we created a Stream Analytics jobs. Now we set up Input, Output and query to extract data:
- Define Input: to get data from IoTHub 
![alt text](screenshots/streamanalytics_input3.png)

![alt text](screenshots/streamanalytics_input4.png)


- Define ouput: to push data to storage account 

![alt text](screenshots/streamanalytics_output2.png)

![alt text](screenshots/streamanalytics_output3.png)

- Create the stream analytics query: 

![alt text](screenshots/streamanalytics_query2.png)

This query processes streaming data in Azure Stream Analytics. It calculates the average of  Surface temperature, snowAccumulation,snowAccumulation, externalTemperature from incoming telemetry data grouped by device IoTHub.ConnectionDeviceId over 60-second intervals using a tumbling window. The results include the device ID, the computed averages, and the event timestamp System.Timestamp. The processed data is then written to an output sink specified by output.

Click Save the query. 

- Start the job: 

In the stream analytics job, click run the job 
![alt text](screenshots/streamanalytics_jobrun.png)

Once the job runs, we can go to check the output
![alt text](screenshots/streamanalytics_jobrun2.png)

Note: We can go to Monitoring menu to check the status of the job

## Step 4: Verify result 
Go to your Azure Storage Account.
Navigate to the container created, verify that processed data is being stored in JSON format.

![alt text](screenshots/streamanalytics_job_checkcontainer.png)

Click on the output JSON file. A new window opens:

![alt text](screenshots/data_generated.png)

Click download JSON to see the result

![alt text](screenshots/data_generated2.png)

We can see the avarage of Surface temperature, snowAccumulation,snowAccumulation, externalTemperature from 3 devices of 3 locations is generated each minute. 

