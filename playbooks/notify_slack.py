import sys
import json

if __name__ == "__main__":
    # The first argument (sys.argv[0]) is the script name itself.
    # The second argument (sys.argv[1]) is the data we pass in.
    if len(sys.argv) > 1:
        alert_data_string = sys.argv[1]
        alert_data = json.loads(alert_data_string)
        print("\n[--- SLACK PLAYBOOK RUNNING ---]")
        print(f"Alert: Notifying Slack about a '{alert_data.get('rule_name')}' event.")
        print(f"Source IP: {alert_data['log_data'].get('source_ip')}")
        print("[--- PLAYBOOK FINISHED ---]\n")