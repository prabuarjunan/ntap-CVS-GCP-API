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
project_number = 123456789  # Enter your project number here
location = "us-central1"
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

def createVolSMB():
    id_token1 = get_token()
    # Get all volumes from all regions
    # Construct GET request

    createvolumeURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Volumes/"
    payload = "{\n  \"name\": \"prabu-smb\",\n  \"region\": \"us-central1\",\n  \"creationToken\": \"prabu-smb\",\n  \"serviceLevel\": \"medium\",\n  \"network\": \"projects/779740114201/global/networks/ncv-vpc\",\n  \"quotaInBytes\": 1099511627776,\n  \"snapReserve\": 20,\n  \"protocolTypes\": [\n    \"CIFS\"\n  ],\n  \"smbShareSettings\": [\n    \"continuously_available\"\n  ],\n  \"jobs\": [\n    {}\n  ],\n  \"labels\": [\n    \"api\"\n  ]\n}\n\n\n"
    headers = {
        'accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    # POST request to create the volume
    response = requests.post(createvolumeURL, payload, headers=headers)
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
    # fetch the class of the protocol types
    ProtocolList = fetchvolumeID.get('protocolTypes')
    # fetch the protocol type
    protocolType = ProtocolList[0]
    # Print the values
    print("\tvolumeID: " + volumeID + ", serviceLevel: " + serviceLevel + ", ProtocolType: " + protocolType)


createVolSMB()
