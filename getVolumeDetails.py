import google.auth
import google.auth.transport.requests
import requests
from google.auth import jwt
from google.oauth2 import service_account

# Set common variables
audience = 'https://cloudvolumesgcp-api.netapp.com'
server = 'https://cloudvolumesgcp-api.netapp.com'
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 123456789
location = "us-central1"
volumeIDdetails = "94b4e74f-37fd-1e9b-b8f9-541e99c6e3e2"

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

def getVolumeDetails():
    id_token1 = get_token()
    # Get all volumes from all regions
    # Construct GET request
    volumeURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Volumes/" + volumeIDdetails
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    response = requests.request("GET", volumeURL, data=payload, headers=headers)
    # Load the json response into a dict
    r_dict = response.json()
    #Print out all service levels
    print("Response to GET request: " + volumeURL)
    # Get volume attributes
    volumeName = (r_dict.get('name'))
    volumeID = (r_dict.get('volumeId'))
    serviceLevcel = (r_dict.get('serviceLevel'))
    print("\tvolumeName: " + volumeName + ", serviceLevel: " + serviceLevcel , "volumeID: " + volumeID)

getVolumeDetails()