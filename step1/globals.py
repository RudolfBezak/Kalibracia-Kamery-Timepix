def load_config(filename):
    config = {}
    try:
      with open(filename, 'r') as file:
          for line in file:
              line = line.strip()
              if line and not line.startswith('#'):  # Ignore empty lines and comments
                  key, value = line.split('=')
                  config[key.strip()] = int(value.strip())  # Convert the value to an integer
    except FileNotFoundError:
        print(f'Súbor {filename} sa nenašiel')
    return config

config = load_config('config.txt')

MAX_TOT = config['MAX_TOT']
THRESHOLD = config['THRESHOLD']
RESOLUTION = config['RESOLUTION']