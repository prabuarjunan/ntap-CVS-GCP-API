# ntap-CVS-GCP-API
The example scripts to use GCP - NetApp Cloud volumes service API to dynamically change the service level on the fly.

# Set common variables
Python interpreter : 3.7
service_account_file = '/Users/arjunan/Downloads/project-beta-demo-xxxxxxxxxxxx.json' #give your file path for json \
project_number = 123456789                                                            #Give your  project number \
location = "us-central1"                                                              #Enter your region here \
volumeIDdetails = "EnteryourVolumeIDhere"                                             #Enter your volume ID here \

 
in def updateServiceLevel(): change the payload based on the change required.
payloadbasic = "{\n    \"serviceLevel\": \"basic\"\n}"
payloadstandard = "{\n    \"serviceLevel\": \"standard\"\n}"
payloadExtreme = "{\n    \"serviceLevel\": \"extreme\"\n}"
 
I still have not made it user friendly. I will do the changes soon.
Let me know if you have any doubts.