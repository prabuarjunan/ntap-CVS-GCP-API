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
ActiveDirectory = "4b4507f4-a71c-6b13-6866-bf46899621e3"
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

def updateAD():
    id_token1 = get_token()
    # Get all volumes from all regions
    # Construct GET request
    updateADURL = server + "/v2/projects/" + str(project_number) + "/locations/" + location + "/Storage/" + "/ActiveDirectory/" + ActiveDirectory
    payload = "{\n    \"username\": \"admin-prabu@cloudheroes.dom\",\n    \"password\": \"Netapp123..!\",\n    \"domain\": \"cloudheroes.dom\",\n    \"DNS\": \"10.3.1.15\",\n    \"netBIOS\": \"cloudier\",\n    \"organizationalUnit\": \"CN=Computers\",\n    \"site\": \"Default-First-Site-Name\",\n    \"kdcIP\": \"10.3.1.15\",\n    \"adName\": \"2BOVAEKB44B\",\n    \"ldapSigning\": false,\n    \"securityOperators\": [\n        \"test\"\n    ],\n    \"backupOperators\": [\n        \"backupOperators1\",\n        \"backupOperators2\"\n    ]\n}"
    headers = {
        'accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer " + id_token1.decode('utf-8'),
        'cache-control': "no-cache",
    }
    # POST request to create the volume
    response = requests.put(updateADURL, payload, headers=headers)
    # Sleep for 20 seconds to wait for the creation of the volume
    time.sleep(20)
    r_dict = response.json()
    # Get AD attributes
    # fetch the DNS details
    DNSServer = (r_dict.get('DNS'))
    # fetch the KPC IP address
    kdcIP = (r_dict.get('kdcIP'))
    # fetch the Domain Name
    domain = (r_dict.get('domain'))
    # fetch the KPC IP address
    UUID = (r_dict.get('UUID'))
    # Print the values
    print("\tDNSServer: " + DNSServer + ", domain: " + domain + ", kdcIP: " + kdcIP + ", UUID: " + UUID)
    backupOperators = (r_dict.get('backupOperators'))
    for backupOperatorsName in backupOperators:
        # get updated backup operators
        print(backupOperatorsName)

updateAD()
