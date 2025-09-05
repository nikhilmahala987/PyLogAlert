# main.py
import json
from core.utils import load_config
from core.collector import read_log_file
from core.parser import parse_log_line
from core.analyzer import analyze_log
from core.responder import trigger_playbook

if __name__ == "__main__":
    config = load_config('config.yaml')
    log_file_path = config['log_sources']['firewall_log']

    print(f"--- Starting analysis of {log_file_path} ---")

    log_generator = read_log_file(log_file_path)

    for line in log_generator:
        parsed_log = parse_log_line(line)

        if parsed_log:
            analysis_result = analyze_log(parsed_log)

            if analysis_result['triggered']:
                playbook_to_run = analysis_result['playbook']
                alert_details = analysis_result
                
                print(f"\n✅ Alert triggered by rule '{alert_details['rule_name']}'. Handing off to responder...")
                trigger_playbook(playbook_to_run, alert_details)

    print("\n--- Analysis complete ---")