import google.auth
import google.auth.transport.requests
from google.auth import jwt
from google.oauth2 import service_account

# Set common variables
audience = 'https://cloudvolumesgcp-api.netapp.com'
server = 'https://cloudvolumesgcp-api.netapp.com'
service_account_file = '/Users/arjunan/Downloads/ncv-beta-demo-eccee8711557.json'
project_number = 779740114201 # staging 779740114201

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
    print("Token:", id_token1)
    return id_token1

get_token()
