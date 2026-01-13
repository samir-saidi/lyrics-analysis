import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# List of artists to analyze
ARTISTS = [
    "Joanna Newsom",
    "Joni Mitchell",
    "Sufjan Stevens",
    "Fiona Apple",
    "Kate Bush",
    "Tori Amos"
]

# Number of songs per artist to fetch
SONGS_PER_ARTIST = 10

# Data storage settings
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed")

# API settings
REQUEST_DELAY = 1  # Seconds between requests to avoid rate limiting
MAX_RETRIES = 3    # Number of retries if request fails