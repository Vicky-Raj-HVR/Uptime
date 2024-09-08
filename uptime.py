import argparse
import requests

API_KEY = 'b9eaabd05817675ee4'

# Helper function to get monitor ID by URL or friendly name
def get_monitor_id_by_url_or_name(url=None, friendly_name=None):
    response = requests.post(
        'https://api.uptimerobot.com/v2/getMonitors',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'api_key': API_KEY, 'format': 'json'}
    )
    monitors = response.json().get('monitors', [])

    for monitor in monitors:
        if url and monitor['url'] == url:
            return monitor['id']
        if friendly_name and monitor['friendly_name'] == friendly_name:
            return monitor['id']
    return None

# Add a new monitor
def add_monitor(friendly_name, url, monitor_type, alert_contacts='', keyword='', keyword_type=None):
    data = {
        'api_key': API_KEY,
        'friendly_name': friendly_name,
        'url': url,
        'type': monitor_type,
        'alert_contacts': alert_contacts,
        'format': 'json'
    }

    if monitor_type == 2:
        if keyword and keyword_type:
            data['keyword'] = keyword
            data['keyword_type'] = keyword_type
        else:
            print("Keyword monitoring requires both 'keyword' and 'keyword_type'. Aborting.")
            return

    response = requests.post(
        'https://api.uptimerobot.com/v2/newMonitor',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data
    )
    result = response.json()
    if result.get('stat') == 'ok':
        print(f"Monitor for '{url}' added successfully.")
    else:
        print(f"Failed to add monitor: {result.get('error', 'Unknown error')}")

# Update existing monitor using URL or friendly name
def update_monitor(friendly_name=None, url=None, new_friendly_name=None, new_url=None, monitor_type=None, alert_contacts=None, keyword=None, keyword_type=None):
    monitor_id = get_monitor_id_by_url_or_name(url=url, friendly_name=friendly_name)

    if not monitor_id:
        print(f"Monitor not found with URL '{url}' or friendly name '{friendly_name}'.")
        return

    data = {
        'api_key': API_KEY,
        'id': monitor_id,
        'format': 'json'
    }

    if new_friendly_name:
        data['friendly_name'] = new_friendly_name
    if new_url:
        data['url'] = new_url
    if monitor_type:
        data['type'] = monitor_type
    if alert_contacts:
        data['alert_contacts'] = alert_contacts

    if monitor_type == 2:
        if keyword and keyword_type:
            data['keyword'] = keyword
            data['keyword_type'] = keyword_type
        else:
            print("Keyword monitoring update requires both 'keyword' and 'keyword_type'.")
            return

    response = requests.post(
        'https://api.uptimerobot.com/v2/editMonitor',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data
    )
    result = response.json()
    if result.get('stat') == 'ok':
        print(f"Monitor '{monitor_id}' updated successfully.")
    else:
        print(f"Failed to update monitor: {result.get('error', 'Unknown error')}")

# Enable or Disable a monitor using URL or friendly name
def set_monitor_status(url=None, friendly_name=None, status=0):
    monitor_id = get_monitor_id_by_url_or_name(url=url, friendly_name=friendly_name)
    
    if monitor_id:
        data = {
            'api_key': API_KEY,
            'id': monitor_id,
            'status': str(status),  # 0 for disable (pause), 1 for enable (resume)
            'format': 'json'
        }
        response = requests.post(
            'https://api.uptimerobot.com/v2/editMonitor',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=data
        )
        result = response.json()
        action = "enabled" if status == 1 else "disabled"
        if result.get('stat') == 'ok':
            print(f"Monitor '{url or friendly_name}' {action} successfully.")
        else:
            print(f"Failed to {action} monitor '{url or friendly_name}': {result.get('error', 'Unknown error')}")
    else:
        print(f"Monitor with URL '{url}' or friendly name '{friendly_name}' not found.")

# Main function to handle actions
def main():
    parser = argparse.ArgumentParser(description="UptimeRobot Monitor Management")
    parser.add_argument('action', choices=['add', 'update', 'enable', 'disable'], help="Action to perform")
    parser.add_argument('--friendly_name', help="Friendly name for the monitor")
    parser.add_argument('--url', help="URL to monitor")
    parser.add_argument('--monitor_type', type=int, choices=[1, 2, 3], help="Type of monitor (1: HTTP(s), 2: Keyword, 3: Ping)")
    parser.add_argument('--alert_contacts', default='', help="Space-separated list of alert contact IDs")
    parser.add_argument('--keyword', default='', help="Keyword for Keyword Monitor (only if MONITOR_TYPE is 2)")
    parser.add_argument('--keyword_type', type=int, choices=[1, 2], help="Keyword type (1: Exists, 2: Not Exists)")
    parser.add_argument('--new_friendly_name', help="New friendly name for update")
    parser.add_argument('--new_url', help="New URL for update")
    
    args = parser.parse_args()

    if args.action == 'add':
        if args.url and args.friendly_name and args.monitor_type:
            add_monitor(
                friendly_name=args.friendly_name,
                url=args.url,
                monitor_type=args.monitor_type,
                alert_contacts=args.alert_contacts,
                keyword=args.keyword,
                keyword_type=args.keyword_type
            )
        else:
            print("Friendly name, URL, and monitor type are required to add a new monitor.")
    
    elif args.action == 'update':
        if args.url or args.friendly_name:
            update_monitor(
                friendly_name=args.friendly_name,
                url=args.url,
                new_friendly_name=args.new_friendly_name,
                new_url=args.new_url,
                monitor_type=args.monitor_type,
                alert_contacts=args.alert_contacts,
                keyword=args.keyword,
                keyword_type=args.keyword_type
            )
        else:
            print("URL or friendly name is required for update.")
    
    elif args.action == 'disable':
        if args.url or args.friendly_name:
            set_monitor_status(url=args.url, friendly_name=args.friendly_name, status=0)
        else:
            print("URL or friendly name is required to disable a monitor.")
    
    elif args.action == 'enable':
        if args.url or args.friendly_name:
            set_monitor_status(url=args.url, friendly_name=args.friendly_name, status=1)
        else:
            print("URL or friendly name is required to enable a monitor.")

if __name__ == '__main__':
    main()
