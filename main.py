import os
from csv_processing import read_csv
from api_clients import send_events, send_identity, get_all_cohorts

def transform_event(event):

    return {
        "name": event.get("name"),
        "time": event.get("time"),  # Must be in ISO 8601 format
        "view_id": event.get("view_id"),
        "session_id": event.get("session_id"),
        "properties": {
            "title": event.get("title")
        }
    }

def build_event_payload(user_id, events):
    return {
        "user_id": user_id,
        "events": events
    }

def transform_identity(identity):
    return {
        "user_id": identity.get("user_id"),
        "identity_id": identity.get("id"),
        "tag": identity.get("tag"),
        "priority": int(identity.get("priority", "0"))
    }

def main():
    # Determine the directory where main.py is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Build file paths to the CSV files in the 'csv_data' folder.
    events_file = os.path.join(script_dir, "csv_data", "events_akel.csv")
    identities_file = os.path.join(script_dir, "csv_data", "identities_akel.csv")
    
    # --- Process Events CSV ---
    raw_events = read_csv(events_file)
    print(f"Processing {len(raw_events)} events from '{events_file}'.")
    
    # Group events by user_id
    events_by_user = {}
    for event in raw_events:
        user_id = event.get("user_id")
        if user_id:
            transformed_event = transform_event(event)
            events_by_user.setdefault(user_id, []).append(transformed_event)
    
    # For each user, build the payload and send it to the segmentation endpoint.
    for user_id, user_events in events_by_user.items():
        payload = build_event_payload(user_id, user_events)
        print(f"Sending events payload for user {user_id}:\n{payload}")
        response = send_events(payload)
        print(f"Response for user {user_id}: {response.status_code}\n{response.text}\n")
    
    # --- Process Identities CSV ---
    raw_identities = read_csv(identities_file)
    print(f"Processing {len(raw_identities)} identities from '{identities_file}'.")
    
    for identity in raw_identities:
        payload = transform_identity(identity)
        print(f"Sending identity payload:\n{payload}")
        response = send_identity(payload)
        print(f"Response for identity: {response.status_code}\n{response.text}\n")
    
    # --- Fetch All Cohorts ---
    print("Fetching all cohorts...")
    cohorts_response = get_all_cohorts()
    print(f"Cohorts API response: {cohorts_response.status_code}")
    print(cohorts_response.text)

if __name__ == "__main__":
    main()
