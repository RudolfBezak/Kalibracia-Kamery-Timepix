import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def load_config(filename):
    default_config = {
        'MAX_TOT': 100,
        'THRESHOLD': 6,
        'RESOLUTION': 256,
        'DEBUG_MODE': 0
    }
    config = {}
    try:
      with open(filename, 'r') as file:
          for line in file:
              line = line.strip()
              if line and not line.startswith('#'):  # Ignore empty lines and comments
                  key, value = line.split('=')
                  config[key.strip()] = int(value.strip())  # Convert the value to an integer
    except FileNotFoundError:
        print(f"[Konfigurácia] Súbor {filename} sa nenašiel, vytváram s predvolenými hodnotami")
        with open(filename, 'w') as file:
            for key, value in default_config.items():
                file.write(f'{key} = {value}\n')
        config = default_config.copy()
    
    for key in default_config:
        if key not in config:
            config[key] = default_config[key]
    
    return config

_config_path = os.path.join(get_base_path(), 'config.txt')
config = load_config(_config_path)

print(f"[Konfigurácia] Nacitane z {_config_path}: MAX_TOT={config['MAX_TOT']}, THRESHOLD={config['THRESHOLD']}, RESOLUTION={config['RESOLUTION']}, DEBUG_MODE={config['DEBUG_MODE']}")

MAX_TOT = config['MAX_TOT']
THRESHOLD = config['THRESHOLD']
RESOLUTION = config['RESOLUTION']
DEBUG_MODE = config['DEBUG_MODE']