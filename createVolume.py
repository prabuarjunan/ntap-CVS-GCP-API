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
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 779740114201
location = "us-central1"
volumeIDdetails = "4f30e00b-87ef-28b3-6e74-72e1c1c378d3"

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
        "name": "AutomatedVolume1",
        "creationToken": "ACV1",
        "region": "us-central1",
        "serviceLevel": "basic",
        "quotaInBytes": 1100000000000,
        "kerberosEnabled": "true",
        "network": "projects/779740114201/global/networks/ncv-vpc",
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
    response = requests.post(createvolumeURL, json.dumps(payload), headers=headers)
    #
    time.sleep(30)
    r_dict = response.json()
    #
    print("Response to POST request: " + response.text)
    # Get volume attributes
    #volumeName = (r_dict.get('name'))
    fetchvalue = (r_dict.get('response'))
    fetchvolumeID = fetchvalue.get('AnyValue')
    volumeID = fetchvolumeID.get('volumeId')
    serviceLevel = fetchvolumeID.get('serviceLevel')
    print("\tvolumeID: " + volumeID + ", serviceLevel: " + serviceLevel)

createVol()