import os

# Data directory path (relative to this config file's location)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# JSON file paths
SAMPLES_FILE = os.path.join(DATA_DIR, "samples.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
