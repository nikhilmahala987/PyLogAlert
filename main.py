# main.py
from core.utils import load_config

if __name__ == "__main__":
    config = load_config('config.yaml')
    print("Configuration loaded successfully:")
    print(config)