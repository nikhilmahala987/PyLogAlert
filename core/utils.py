import yaml
import os

def load_config(a):
    config_path = os.path.join(os.path.dirname(__file__), '..', a)
    config_path = os.path.abspath(config_path)
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)  # 'safe_load' is the secure method
    # 2. Now 'config_data' is a native Python dictionary!
    return(config_data)
    # Output: {'log_source': '/var/log/my_app/app.log', 'alert_threshold': 5, ...}