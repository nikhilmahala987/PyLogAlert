# main.py
from core.utils import load_config
from core.collector import read_log_file

if __name__ == "__main__":
    config = load_config('config.yaml')
    log_file_path = config['log_sources']['firewall_log']
    log_generator = read_log_file(log_file_path)
    for line in log_generator:
        print(line.strip())
    print("Configuration loaded successfully:")
    print(config)