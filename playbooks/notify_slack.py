import sys
import json
import requests
sys.path.append('.')
from core.utils import load_config

def send_slack_notification(webhook_url, alert_data):
    
    rule_name = alert_data.get('rule_name', 'Unknown Rule')
    source_ip = alert_data.get('log_data', {}).get('source_ip', 'N/A')
    
    message_text = f"🚨 Mini-SOAR Alert: '{rule_name}' triggered from IP `{source_ip}`."
    
    slack_payload = {
        "text": message_text, # Fallback text for notifications
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 Mini-SOAR Alert"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Rule Name:*\n{rule_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Source IP:*\n`{source_ip}`"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Full Log Data:*\n```\n{json.dumps(alert_data['log_data'], indent=2)}\n```"
                }
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=slack_payload, timeout=5)
        response.raise_for_status()
        print("Notification sent to Slack successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Slack: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python notify_slack.py '<alert_json_string>'")
        sys.exit(1)
        
    alert_json_string = sys.argv[1]
    try:
        alert_data = json.loads(alert_json_string)
    except json.JSONDecodeError:
        print("Error: Invalid JSON data provided.")
        sys.exit(1)
        
    config = load_config('config.yaml')
    webhook_url = config.get('slack_webhook_url')
    
    if not webhook_url or not webhook_url.startswith("https://hooks.slack.com"):
        print("Error: 'slack_webhook_url' not found or invalid in config.yaml.")
        sys.exit(1)
        
    send_slack_notification(webhook_url, alert_data)