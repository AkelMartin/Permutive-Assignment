import requests

API_KEY = '438f9c00-7273-416d-a22c-f01c02f682ae'

# Endpoint for sending segmentation events.
EVENTS_ENDPOINT_URL = (
    "https://api.permutive.app/ccs/v1/segmentation"
)

# Endpoint for identities (using the same base segmentation endpoint)
IDENTITY_ENDPOINT_URL = "https://api.permutive.app/ccs/v1/segmentation"

# Endpoint for retrieving all cohorts.
COHORTS_ENDPOINT_URL = "https://api.permutive.app/cohorts-api/v2/cohorts"

def send_events(payload):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(EVENTS_ENDPOINT_URL, json=payload, headers=headers)
    return response

def send_identity(payload):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(IDENTITY_ENDPOINT_URL, json=payload, headers=headers)
    return response

def get_all_cohorts():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.get(COHORTS_ENDPOINT_URL, headers=headers)
    return response
