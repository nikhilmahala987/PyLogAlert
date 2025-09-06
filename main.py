import json
from core.utils import load_config
from core.collector import read_log_file
from core.parser import parse_log_line
# --- Step 1: Change the import ---
# We now import the RuleEngine class instead of the old function.
from core.analyzer import RuleEngine
from core.responder import trigger_playbook

if __name__ == "__main__":
    config = load_config('config.yaml')
    log_file_path = config['log_sources']['firewall_log']

    print(f"--- Starting PyLogAlert Engine ---")

    # --- Step 2: Initialize the engine once at the start ---
    # This creates an instance of our engine.
    # The engine will automatically load all the .yml files from the /rules directory.
    rule_engine = RuleEngine()

    print(f"\n--- Monitoring log file: {log_file_path} ---")

    log_generator = read_log_file(log_file_path)

    for line in log_generator:
        parsed_log = parse_log_line(line)

        if parsed_log:
            # --- Step 3: Call the analyze_log method from our engine instance ---
            analysis_result = rule_engine.analyze_log(parsed_log)

            if analysis_result['triggered']:
                playbook_to_run = analysis_result['playbook']
                alert_details = analysis_result
                
                print(f"\n✅ Alert triggered by rule '{alert_details['rule_name']}'. Handing off to responder...")
                trigger_playbook(playbook_to_run, alert_details)

    print("\n--- Analysis complete ---")