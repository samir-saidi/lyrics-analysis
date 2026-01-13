# scripts/get_lyrics.py
import os
import sys
import time
import json
import pandas as pd
from dotenv import load_dotenv
import lyricsgenius
from ftfy import fix_encoding

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Configuration settings below:

# List of artists to analyze
# TODO: Expand this list
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


# Load environment variables
env_path = os.path.join(PROJECT_ROOT, '.env')
print(f"Looking for .env at: {env_path}")
print(f".env exists: {os.path.exists(env_path)}")

load_dotenv(dotenv_path=env_path)

class LyricsCollector:
    def __init__(self):
        """Initialize the Genius API client"""
        token = os.getenv("GENIUS_ACCESS_TOKEN")
        if not token:
            raise ValueError("GENIUS_ACCESS_TOKEN not found in .env file")
        
        self.genius = lyricsgenius.Genius(token)
        self.configure_genius()

        #Track what we've collected so far
        self.collection_log = []

    def configure_genius(self):
        """Configure the Genius client"""
        self.genius.remove_section_headers = True # Remove [Chorus], etc.
        self.genius.skip_non_songs = True # Skip interviews, etc.
        self.genius.excluded_terms = [ # Exclude live versions, remixes, etc.
            "(Live)", "(Remix)", "(Demo)", 
            "(Acoustic)", "(Instrumental)"
        ] 
        # Add timeout and retry settings
        self.genius.timeout = 30
        self.genius.retries = 3
    
    def fetch_artist(self, artist_name, max_songs):
        """Fetch artist, supports error handling and retries"""
        for attempt in range(MAX_RETRIES):
            try:
                print(f"Attempt {attempt + 1}/{MAX_RETRIES} for {artist_name}...")
                
                artist = self.genius.search_artist(
                    artist_name, 
                    max_songs=max_songs,
                    sort="popularity",
                    include_features=False  # Only songs where they're primary artist
                )
                
                if artist and artist.songs:
                    return artist
                elif artist and not artist.songs:
                    print(f"  Warning: Found artist but no songs")
                    return None
                    
            except Exception as e:
                print(f"  Error on attempt {attempt + 1}: {str(e)[:100]}...")
                if attempt < MAX_RETRIES - 1:
                    wait_time = REQUEST_DELAY * (attempt + 1) * 2  # Exponential backoff
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"Failed after {MAX_RETRIES} attempts")
        
        return None

    def collect_artist(self, artist_name, max_songs=SONGS_PER_ARTIST):
        """Collect all songs for one artist"""
        print(f"\n{'='*50}")
        print(f"Collecting songs for: {artist_name}")
        print(f"{'='*50}")
        
        start_time = time.time()
        artist = self.fetch_artist(artist_name, max_songs)
        
        if not artist or not artist.songs:
            print(f"Failed to collect songs for {artist_name}")
            self.collection_log.append({
                "artist": artist_name,
                "status": "failed",
                "songs_collected": 0,
                "time_taken": time.time() - start_time
            })
            return []
        
        # Save each song
        saved_songs = []
        for i, song in enumerate(artist.songs, 1):
            try:
                # Get additional song info
                song_info = self.extract_song_info(song, artist_name)
                
                # Save lyrics to file
                lyrics_path = self.save_lyrics(song, artist_name)
                
                # Save metadata
                metadata_path = self.save_metadata(song_info, artist_name)
                
                saved_songs.append(song_info)
                
                print(f"[{i}/{len(artist.songs)}] {song.title}")
                
                # Small delay between songs to be nice to the API
                time.sleep(REQUEST_DELAY)
                
            except Exception as e:
                print(f"Error saving song {song.title}: {str(e)[:100]}")
        
        # Log this collection
        self.collection_log.append({
            "artist": artist_name,
            "status": "success",
            "songs_collected": len(saved_songs),
            "time_taken": time.time() - start_time
        })
        
        print(f"\nSuccessfully collected {len(saved_songs)} songs for {artist_name}")
        return saved_songs
    
    def extract_song_info(self, song, artist_name):
        """Extract relevant information from a song object"""
        # Fixes encoding problems
        lyrics = fix_encoding(song.lyrics) if song.lyrics else "" 
        return {
            "artist": artist_name,
            "title": song.title,
            "album": getattr(song, 'album', None).get('name'),
            "lyrics": lyrics,
            "lyrics_length": len(lyrics.split()),
        }
    
    def save_lyrics(self, song, artist_name):
        """Save lyrics to a text file"""
        # Create artist folder
        safe_artist_name = artist_name.replace(" ", "_").replace("/", "_")
        artist_folder = os.path.join(RAW_DATA_PATH, "lyrics", safe_artist_name)
        os.makedirs(artist_folder, exist_ok=True)
        
        # Create safe filename
        safe_title = "".join(c for c in song.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}.txt"
        filepath = os.path.join(artist_folder, filename)
        
        # Save lyrics
        with open(filepath, "w", encoding="utf-8") as f:
            # Fixes encoding problems
            lyrics = fix_encoding(song.lyrics) if song.lyrics else "" 
            f.write(lyrics)
        
        return filepath
    
    def save_metadata(self, song_info, artist_name):
        """Save song metadata to JSON"""
        # Create metadata folder
        safe_artist_name = artist_name.replace(" ", "_").replace("/", "_")
        metadata_folder = os.path.join(RAW_DATA_PATH, "metadata", safe_artist_name)
        os.makedirs(metadata_folder, exist_ok=True)
        
        # Create safe filename
        safe_title = "".join(c for c in song_info["title"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}.json"
        filepath = os.path.join(metadata_folder, filename)
        
        # Save metadata (without full lyrics to keep file small)
        metadata = song_info.copy()
        del metadata["lyrics"]  # Don't duplicate lyrics in metadata
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        return filepath
    
    def save_collection_summary(self):
        """Save a summary of what was collected"""
        summary_path = os.path.join(PROCESSED_DATA_PATH, "collection_summary.csv")
        
        df = pd.DataFrame(self.collection_log)
        df.to_csv(summary_path, index=False, encoding='utf-8')
        print(f"\nCollection summary saved to: {summary_path}")
        
        # Print summary
        print("\n" + "="*50)
        print("COLLECTION SUMMARY")
        print("="*50)
        for log in self.collection_log:
            status_icon = "Success!" if log["status"] == "success" else "Failed..."
            print(f"{status_icon} {log['artist']}: {log['songs_collected']} songs "
                    f"({log['time_taken']:.1f}s)")

def collect_all_artists():
    """Main function to collect data for all artists"""
    print("Starting lyrics collection pipeline...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Artists: {', '.join(ARTISTS)}")
    print(f"Songs per artist: {SONGS_PER_ARTIST}")
    
    # Create necessary directories - use absolute paths
    os.makedirs(os.path.join(RAW_DATA_PATH, "lyrics"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DATA_PATH, "metadata"), exist_ok=True)
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    
    collector = LyricsCollector()
    all_songs = []
    
    # Collect for each artist
    for artist in ARTISTS:
        songs = collector.collect_artist(artist, SONGS_PER_ARTIST)
        all_songs.extend(songs)
        
        # Save intermediate results after each artist
        if songs:
            temp_df = pd.DataFrame(songs)
            temp_path = os.path.join(PROCESSED_DATA_PATH, f"collected_{artist.replace(' ', '_')}.csv")
            temp_df.to_csv(temp_path, index=False, encoding='utf-8')
            print(f"Intermediate save: {temp_path}")
    
    # Save final results
    if all_songs:
        final_df = pd.DataFrame(all_songs)
        final_path = os.path.join(PROCESSED_DATA_PATH, "all_songs_raw.csv")
        final_df.to_csv(final_path, index=False, encoding='utf-8')
        print(f"\nAll songs saved to: {final_path}")
        print(f"Total songs collected: {len(all_songs)}")
    
    # Save collection log
    collector.save_collection_summary()
    
    return all_songs

def test_with_one_artist():
    """Test function: collect data for just one artist"""
    print("Running test with one artist...")
    
    # Temporarily modify config for testing
    test_artists = ["Joanna Newsom"]
    test_songs_per = 3
    
    # Create necessary directories
    os.makedirs(os.path.join(RAW_DATA_PATH, "lyrics"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DATA_PATH, "metadata"), exist_ok=True)
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    collector = LyricsCollector()
    
    print(f"Testing with: {test_artists[0]} ({test_songs_per} songs)")
    songs = collector.collect_artist(test_artists[0], test_songs_per)
    
    if songs:
        # Save test results
        test_df = pd.DataFrame(songs)
        test_path = os.path.join(PROCESSED_DATA_PATH, "test_collection.csv")
        test_df.to_csv(test_path, index=False, encoding='utf-8')
        
        print(f"\nTest successful!")
        print(f"Songs collected: {len(songs)}")
        print(f"Data saved to: {test_path}")
        
        # Show sample
        print("\nSample data:")
        print(test_df[["artist", "title", "lyrics_length"]].head())
        
        # Check the data folder
        print(f"\nCheck your data folder:")
        print(f"Raw lyrics: {RAW_DATA_PATH}/lyrics/")
        print(f"Metadata: {RAW_DATA_PATH}/metadata/")
    
    return songs

if __name__ == "__main__":
        # Ask user what to do
        print("Choose an option:")
        print("1. Test with one artist (3 songs)")
        print("2. Collect all artists (10 songs each)")
        print("3. Custom collection")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            test_with_one_artist()
        elif choice == "2":
            collect_all_artists()
        elif choice == "3":
            # You could add custom logic here
            print("Custom collection not implemented yet. Running test instead.")
            test_with_one_artist()
        else:
            print("Invalid choice. Running test with one artist.")
            test_with_one_artist()