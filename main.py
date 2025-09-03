# main.py
import json
from core.utils import load_config
from core.collector import read_log_file
from core.parser import parse_log_line
from core.analyzer import analyze_log

if __name__ == "__main__":
    config = load_config('config.yaml')
    log_file_path = config['log_sources']['firewall_log']

    print(f"--- Starting analysis of {log_file_path} ---")

    log_generator = read_log_file(log_file_path)

    # Process each log line
    for line in log_generator:
        parsed_log = parse_log_line(line)
        print(json.dumps(parsed_log, indent=4))
        # If the parser returns a valid dictionary (not None)...
        if parsed_log:
            analysis_result = analyze_log(parsed_log)

            # If the analyzer triggered a rule...
            if analysis_result['triggered']:
                # ...print a formatted alert!
                print("\n" + "─" * 40)
                print(f"🚨 ALERT! Rule '{analysis_result['rule_name']}' triggered.")
                print("─" * 40)
                print(json.dumps(parsed_log, indent=4))
                print("─" * 40 + "\n")

    print("--- Analysis complete ---")