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
project_number = 1234567890 # Enter your project number here
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

def deleteVol():
    id_token1 = get_token()
    # Construct delete request
    deletevolumeURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Volumes/" + volumeIDdetails
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    # delete request to create the volume
    response = requests.request("DELETE", deletevolumeURL, headers=headers, data=payload)
    print(response.text)

deleteVol()
