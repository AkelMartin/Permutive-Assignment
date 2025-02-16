import os
from csv_processing import read_csv
from api_clients import send_events, send_identity, get_all_cohorts

def transform_event(event):
    
    def split_to_list(value):
        if value:
            return [item.strip() for item in value.split(",") if item.strip()]
        else:
            return []
    
    event_json = {}
    event_json["name"] = event.get("name")
    event_json["user_id"] = event.get("user_id")
    event_json["properties"] = {
        "articleType": event.get("articleType"),
        "client": {
            "domain": event.get("domain"),
            "referrer": event.get("referrer"),
            "title": event.get("title"),
            "type": event.get("type"),
            "url": event.get("url"),
            "user_agent": event.get("user_agent")
        },
        "geo_info": {
            "city": event.get("city"),
            "continent": event.get("continent"),
            "country": event.get("country"),
            "postal_code": event.get("postal_code"),
            "province": event.get("province")
        },
        "isp_info": {
            "autonomous_system_number": int(event.get("autonomous_system_number", 0)) if event.get("autonomous_system_number") else None,
            "autonomous_system_organization": event.get("autonomous_system_organization"),
            "isp": event.get("isp"),
            "organization": event.get("organization")
        },
        "contentTags": split_to_list(event.get("contentTags"))
    }
    event_json["session_id"] = event.get("session_id")
    event_json["view_id"] = event.get("view_id")
    event_json["time"] = event.get("time")
    event_json["segments"] = [int(x) for x in split_to_list(event.get("segments"))] if event.get("segments") else []
    event_json["cohorts"] = split_to_list(event.get("cohorts"))
    event_json["id"] = event.get("id")
    
    return event_json

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
    # Determine the directory where main.py is located.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Build file paths to the CSV files in the 'csv_data' folder.
    events_file = os.path.join(script_dir, "csv_data", "events_akel.csv")
    identities_file = os.path.join(script_dir, "csv_data", "identities_akel.csv")
    
    # --- Process Events CSV ---
    raw_events = read_csv(events_file)
    print(f"Processing {len(raw_events)} events from '{events_file}'.")
    
    # Group events by user_id.
    events_by_user = {}
    for event in raw_events:
        user_id = event.get("user_id")
        if user_id:
            transformed_event = transform_event(event)
            events_by_user.setdefault(user_id, []).append(transformed_event)
        else:
            print("Warning: Event row missing 'user_id'. Skipping row.")
    
    # For each user, build the payload and send it.
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
