import google.auth
import google.auth.transport.requests
import requests
import time
from google.auth import jwt
from google.oauth2 import service_account

# Set common variables
audience = 'https://cloudvolumesgcp-api.netapp.com'
server = 'https://cloudvolumesgcp-api.netapp.com'
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 1234567890  # Enter your project number here
location = "us-central1"
volumeIDdetails = "7fd1095f-617b-819a-f9ce-e3c84e31b8c9"

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

def updateVolume():
    id_token1 = get_token()
    # Get all volumes from all regions
    # Construct GET request

    updatevolumeURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Volumes/" + volumeIDdetails
    payload = "{\n   \"name\": \"AutomatedVolume1\",\n   \"creationToken\": \"ACV1\",\n   \"region\": \"us-central1\",\n   \"serviceLevel\": \"standard\",\n   \"quotaInBytes\": 1100000000000,\n   \"kerberosEnabled\": \"false\",\n   \"network\": \"projects/123456789/global/networks/ncv-vpc\",\n   \"kerberosEnabled\": \"false\",\n   \"protocolTypes\": [\"NFSv4\"],\n   \"exportPolicy\": {\n      \"rules\": [\n         {\n            \"access\": \"ReadWrite\",\n            \"allowedClients\": \"0.0.0.0/0\",\n             \"hasRootAccess\": false,\n        \"nfsv3\": {\n               \"checked\": false\n            },\n            \"nfsv4\": {\n               \"checked\": true\n            }\n         }\n      ]\n   }\n}"
    headers = {
        'accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    # POST request to create the volume
    response = requests.put(updatevolumeURL, payload, headers=headers)
    # Sleep for 20 seconds to wait for the creation of the volume
    time.sleep(20)
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

updateVolume()