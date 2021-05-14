# Note: Enter the volume size in exact multiples of 1GiB (1024^3).
# In the below example, the volume size specified for “quotaInBytes”is 1099511627776, which is 1024 GiB.
import google.auth
import google.auth.transport.requests
import requests
import json
import time
from google.auth import jwt
from google.oauth2 import service_account

# Set common variables
audience = 'https://cloudvolumesgcp-api.netapp.com'
server = 'https://cloudvolumesgcp-api.netapp.com'
# Enter your service account file below
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 123456789  # Enter your project number here
location = "us-east1"
volumeIDdetails = "Enter your Volume ID here"

# Small utility function to convert bytes to gibibytes
def convertToGiB(bytes):
    return bytes/1024/1024/1024

def get_token():
    # Create credential object from private key file
    svc_creds = service_account.Credentials.from_service_account_file(
        service_account_file)

    # Create jwt
    jwt_creds = jwt.Credentials.from_signing_credentials(
        svc_creds, audience=audience)

    # Issue request to get auth token
    request = google.auth.transport.requests.Request()
    jwt_creds.refresh(request)

    # Extract token
    id_token1 = jwt_creds.token
    #print (id_token1)
    return id_token1

def createVol():
    id_token1 = get_token()
    # Get all volumes from all regions
    # Construct GET request

    createvolumeURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Volumes/"
    payload = {
        "name": "AutomatedVolume3",
        "creationToken": "ACV3",
        "region": "us-east1",
        "zone": "us-east1-b",
        "serviceLevel": "basic",
        "quotaInBytes": 1099511627776,
        "usedBytes": 78606279278,
        "snapshotPolicy": {
            "dailySchedule": {
                "hour": 1,
                "minute": 10,
                "snapshotsToKeep": 5
            }
        },
        "storageClass": "software",
        "network": "projects/123456789/global/networks/ncv-vpc", # Replace with your VPC instead of ncv-vpc and the project number instead of 123456789
        "protocolTypes": [
            "NFSv3"
        ]
    }
    headers = {
        'accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    # POST request to create the volume
    response = requests.post(createvolumeURL, json.dumps(payload), headers=headers)
    # Sleep for 20 seconds to wait for the creation of the volume
    time.sleep(20)
    print(response)
    r_dict = response.json()
    # print("Response to POST request: " + response.text)
    # Get volume attributes
    # To get the values from the dictionary, you have read the dictionary one by one.
    # fetch the response first
    fetchvalue = (r_dict.get('response'))
    # fetch all the values from the response
    fetchvolumeID = fetchvalue.get('AnyValue')
    # fetch the volume ID from the values
    volumeID = fetchvolumeID.get('volumeId')
    # fetch the service level from the values
    serviceLevel = fetchvolumeID.get('serviceLevel')
    # Print the values
    print("\tvolumeID: " + volumeID + ", serviceLevel: " + serviceLevel)

createVol()
