import os
import yaml

class RuleEngine:
    def __init__(self, rules_directory="rules/"):
        self.rules = self._load_rules(rules_directory)
        if self.rules:
            print(f"✅ Rule Engine initialized. Loaded {len(self.rules)} rules.")
        else:
            print(f"⚠️ Rule Engine initialized, but no rules were loaded from '{rules_directory}'.")

    def _load_rules(self, directory):
        loaded_rules = []
        
        # --- START OF OUR DEBUGGING CODE ---
        print("\n" + "="*50)
        print("--- ANALYZER DEBUGGER ACTIVATED ---")
        
        # 1. Let's see what the script thinks its CURRENT FOLDER is.
        current_working_directory = os.getcwd()
        print(f"Current Working Directory: {current_working_directory}")
        
        # 2. Let's see if the 'rules' directory exists from here.
        rules_path_to_check = os.path.join(current_working_directory, directory)
        print(f"Checking for rules directory at: {rules_path_to_check}")
        print(f"Does the 'rules' directory exist? -> {os.path.isdir(rules_path_to_check)}")
        
        # 3. Let's get the list of files the script is seeing inside 'rules'.
        # This is the most important piece of evidence.
        try:
            files_in_rules_dir = os.listdir(directory)
            print(f"Files found inside '{directory}': {files_in_rules_dir}")
        except FileNotFoundError:
            print(f"CRITICAL: The directory '{directory}' does not exist from the script's perspective.")
        
        print("="*50 + "\n")
        # --- END OF OUR DEBUGGING CODE ---

        try:
            for filename in os.listdir(directory):
                if filename.endswith(".yml") or filename.endswith(".yaml"):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'r') as f:
                        rule = yaml.safe_load(f)
                        loaded_rules.append(rule)
        except FileNotFoundError:
            # This part will likely not be reached if the above check fails, but it's here for safety.
            pass
            
        return loaded_rules

    def analyze_log(self, parsed_log):
        # ... (rest of the file is the same) ...
        if not parsed_log:
            return {'triggered': False}
        for rule in self.rules:
            if parsed_log.get('process_name') == rule.get('log_source'):
                message = parsed_log.get('message', '')
                for keyword in rule.get('detection', {}).get('keywords', []):
                    if keyword in message:
                        return {
                            'triggered': True,
                            'rule_name': rule.get('rule_name'),
                            'playbook': rule.get('playbook'),
                            'log_data': parsed_log
                        }
        return {'triggered': False}

