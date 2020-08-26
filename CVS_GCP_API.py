import google.auth
import google.auth.transport.requests
import requests
import json
from google.auth import jwt
from google.oauth2 import service_account
from google.oauth2 import id_token
import time

# Set common variables
audience = 'https://cloudvolumesgcp-api.netapp.com'
server = 'https://cloudvolumesgcp-api.netapp.com'
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 123456789
location = "us-central1"
volumeIDdetails = "EnteryourVolumeIDhere"
payloadbasic = "{\n    \"serviceLevel\": \"basic\"\n}"
payloadstandard = "{\n    \"serviceLevel\": \"standard\"\n}"
payloadExtreme = "{\n    \"serviceLevel\": \"extreme\"\n}"


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


def list_volumes():
    id_token1 = get_token()
    # Get all volumes from all regions
    get_url = server + "/v2/projects/" + str(project_number) + "/locations/-/Volumes"
    # Construct GET request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + id_token1.decode('utf-8')
    }
    # Issue the request to the server
    r = requests.get(get_url, headers=headers)
    # Load the json response into a dict
    r_dict = r.json()

    # Print out all vols
    print("Response to GET request: " + get_url)
    for vol in r_dict:
        # Get volume attributes
        volname = vol["name"]
        volID = vol["volumeId"]
        volsizeGiB = convertToGiB(vol["quotaInBytes"])
        region = vol["region"]
        print("\tvolname: " + volname + ", \tvolumeId: " + volID + ", size: " + str(volsizeGiB) + "GiB, region: " + region)

def getServiceLevel():
    id_token1 = get_token()
    # Get service levels
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

def getVolumeDetails():
    id_token1 = get_token()
    # Get all volumes details
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


def updateServiceLevel():
    id_token1 = get_token()
    # update the service level of the volume
    # Construct GET request
    volumeURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Volumes/" + volumeIDdetails
    #payload = "{\n    \"serviceLevel\": \"basic\"\n}"
    payload = payloadbasic
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    response = requests.request("PUT", volumeURL, data=payload, headers=headers)
    # Load the json response into a dict
    #Print out all service levels
    time.sleep(10)
    print("Response to GET request: " + volumeURL)


#get_token()
list_volumes()
getServiceLevel()
updateServiceLevel()
getVolumeDetails()