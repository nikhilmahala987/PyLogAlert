# main.py
import json
from core.utils import load_config
from core.collector import read_log_file
from core.parser import parse_log_line

if __name__ == "__main__":
    config = load_config('config.yaml')
    log_file_path = config['log_sources']['firewall_log']
    log_generator = read_log_file(log_file_path)
    for line in log_generator:
        # # line=line.strip()

        # # 4. Try to parse the line using your parser (Day 4)
        parsed_log = parse_log_line(line)

        # 5. Check the result and print
        if parsed_log:
            # If the parser returns a dictionary, print it nicely
            print("\n✅ Parsed Log Entry:")
            print(json.dumps(parsed_log, indent=4))
        else:
            # If the parser returns None, print the raw line
            print(f"\n❌ Could not parse line: '{line}'")