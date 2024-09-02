import os
import requests

API_KEY = 'd05817675ee4'

# Retrieve monitor by friendly name
def get_monitor_by_friendly_name(friendly_name):
    response = requests.post(
        'https://api.uptimerobot.com/v2/getMonitors',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'api_key': API_KEY, 'format': 'json'}
    )
    monitors = response.json().get('monitors', [])
    
    for monitor in monitors:
        if monitor['friendly_name'] == friendly_name:
            return monitor
    return None

# Retrieve monitor by URL
def get_monitor_by_url(url):
    response = requests.post(
        'https://api.uptimerobot.com/v2/getMonitors',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'api_key': API_KEY, 'format': 'json'}
    )
    monitors = response.json().get('monitors', [])
    
    for monitor in monitors:
        if monitor['url'] == url:
            return monitor
    return None

# Add a new monitor
def add_monitor(friendly_name, url, monitor_type, alert_contacts=None, keyword=None, keyword_type=None):
    data = {
        'api_key': API_KEY,
        'friendly_name': friendly_name,
        'url': url,
        'type': monitor_type,
        'alert_contacts': alert_contacts,
        'keyword_value': keyword,
        'keyword_type': keyword_type
    }
    
    response = requests.post(
        'https://api.uptimerobot.com/v2/newMonitor',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data
    )
    
    result = response.json()
    
    if result.get('stat') == 'ok':
        print(f"Monitor '{friendly_name}' added successfully.")
    else:
        print(f"Failed to add monitor '{friendly_name}': {result.get('error', 'Unknown error')}")

# Update monitor details
def update_monitor(monitor_id, friendly_name=None, url=None, monitor_type=None, alert_contacts=None, keyword=None, keyword_type=None):
    data = {
        'api_key': API_KEY,
        'id': monitor_id,
    }

    if friendly_name:
        data['friendly_name'] = friendly_name
    if url:
        data['url'] = url
    if monitor_type:
        data['type'] = monitor_type
    if alert_contacts:
        data['alert_contacts'] = alert_contacts
    if keyword:
        data['keyword_value'] = keyword
    if keyword_type:
        data['keyword_type'] = keyword_type

    response = requests.post(
        'https://api.uptimerobot.com/v2/editMonitor',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data
    )
    result = response.json()
    
    if result.get('stat') == 'ok':
        print(f"Monitor {monitor_id} updated successfully.")
    else:
        print(f"Failed to update monitor {monitor_id}: {result.get('error', 'Unknown error')}")

# Enable or disable monitor
def set_monitor_status(monitor_id, status):
    data = {
        'api_key': API_KEY,
        'id': monitor_id,
        'status': status  # 0 for pause, 1 for resume
    }
    
    response = requests.post(
        'https://api.uptimerobot.com/v2/editMonitor',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data
    )
    
    result = response.json()
    
    if result.get('stat') == 'ok':
        print(f"Monitor {monitor_id} {'enabled' if status == 1 else 'disabled'} successfully.")
    else:
        print(f"Failed to change status for monitor {monitor_id}: {result.get('error', 'Unknown error')}")

# Main function to handle actions based on friendly name or URL
def main():
    action = os.getenv('ACTION')
    friendly_name = os.getenv('FRIENDLY_NAME')
    url = os.getenv('URL')
    monitor_type = os.getenv('MONITOR_TYPE')
    alert_contacts = os.getenv('ALERT_CONTACTS')
    keyword = os.getenv('KEYWORD')
    keyword_type = os.getenv('KEYWORD_TYPE')

    monitor = None
    if friendly_name:
        monitor = get_monitor_by_friendly_name(friendly_name)
    elif url:
        monitor = get_monitor_by_url(url)

    if action == 'ADD':
        add_monitor(
            friendly_name=friendly_name,
            url=url,
            monitor_type=monitor_type,
            alert_contacts=alert_contacts,
            keyword=keyword,
            keyword_type=keyword_type
        )
    elif monitor:
        monitor_id = monitor['id']
        if action == 'ENABLE':
            set_monitor_status(monitor_id, status=1)
        elif action == 'DISABLE':
            set_monitor_status(monitor_id, status=0)
        elif action == 'UPDATE':
            update_monitor(
                monitor_id=monitor_id,
                friendly_name=friendly_name,
                url=url,
                monitor_type=monitor_type,
                alert_contacts=alert_contacts,
                keyword=keyword,
                keyword_type=keyword_type
            )
        else:
            print("Invalid action.")
    else:
        if action in ['UPDATE', 'ENABLE', 'DISABLE']:
            print("Monitor not found.")
        elif action == 'ADD':
            add_monitor(
                friendly_name=friendly_name,
                url=url,
                monitor_type=monitor_type,
                alert_contacts=alert_contacts,
                keyword=keyword,
                keyword_type=keyword_type
            )
        else:
            print("Invalid action.")

if __name__ == "__main__":
    main()
