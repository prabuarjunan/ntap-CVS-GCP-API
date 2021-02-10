import google.auth
import google.auth.transport.requests
import requests
from google.auth import jwt
from google.oauth2 import service_account

# Set common variables
stagingaudience = 'https://dev-cloudvolumesgcp-api.netapp.com'
audience = 'https://cloudvolumesgcp-api.netapp.com'
server = 'https://cloudvolumesgcp-api.netapp.com'
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 779740114201
location = "us-central1"

# Small utility function to convert bytes to gibibytes
def convertToGiB(bytes):
    return bytes/1024/1024/1024

def get_token():
    # Create credential object from private key file
    svc_creds = service_account.Credentials.from_service_account_file(
        service_account_file)

    # Create jwt
    jwt_creds = jwt.Credentials.from_signing_credentials(
        svc_creds, audience=stagingaudience)

    # Issue request to get auth token
    request = google.auth.transport.requests.Request()
    jwt_creds.refresh(request)

    # Extract token
    id_token1 = jwt_creds.token
    #print (id_token1)
    return id_token1

def getServiceLevel():
    id_token1 = get_token()
    # Get all volumes from all regions
    url = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Storage/ServiceLevels"
    # Construct GET request
    #url = "https://cloudvolumesgcp-api.netapp.com/v2/projects/779740114201/locations/us-central1/Storage/ServiceLevels"
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    # Load the json response into a dict
    r_dict = response.json()
    # Print out all service levels
    print("Response to GET request: " + url)
    for serviceLevel in r_dict:
        # Get volume attributes
        serviceLevelName = serviceLevel["name"]
        serviceLevelPerformance = serviceLevel["performance"]
        print("\tserviceLevelName: " + serviceLevelName + ", \tserviceLevelPerformance: " + serviceLevelPerformance)

getServiceLevel()