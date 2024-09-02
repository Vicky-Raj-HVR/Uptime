import requests

# UptimeRobot API key
API_KEY = 'u2666504-ce8646b9eaabd05817675ee4'

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

# Example usage based on friendly name or URL
monitor = get_monitor_by_friendly_name('Example Monitor')
# Alternatively: monitor = get_monitor_by_url('https://example.com')

if monitor:
    update_monitor(
        monitor_id=monitor['id'],  # You still need to use the ID after finding the monitor
        friendly_name='Updated Monitor Name',
        url='https://new-url-to-monitor.com',
        monitor_type=1,
        alert_contacts='1234 5678 9012',
        keyword='example',
        keyword_type=1
    )
else:
    print("Monitor not found.")

