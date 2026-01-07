# scripts/get_lyrics.py
import os
import sys
import time
from dotenv import load_dotenv
import lyricsgenius

# Add project root to Python path so we can import from other folders
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

class LyricsCollector:
    def __init__(self):
        """Initialize the Genius API client"""
        token = os.getenv("GENIUS_ACCESS_TOKEN")
        if not token:
            raise ValueError("GENIUS_ACCESS_TOKEN not found in .env file")
        
        self.genius = lyricsgenius.Genius(token)
        # Configure the client
        self.genius.remove_section_headers = True  # Remove [Chorus], etc.
        self.genius.skip_non_songs = True  # Skip interviews, etc.
        self.genius.excluded_terms = ["(Live)", "(Remix)"]  # Exclude live versions
        
    def get_artist_songs(self, artist_name, max_songs=10):
        """Get songs for a specific artist"""
        print(f"Fetching songs for {artist_name}...")
        
        artist = self.genius.search_artist(
            artist_name, 
            max_songs=max_songs,
            sort="popularity"  # Get popular songs first
        )
        
        if artist:
            print(f"Successfully fetched {len(artist.songs)} songs by {artist.name}")
            return artist.songs
        else:
            print(f"Could not find artist: {artist_name}")
            return []
    
    def save_song(self, song, artist_name):
        """Save a song's lyrics to a file"""
        # Create artist folder if it doesn't exist
        artist_folder = os.path.join("data", "raw", artist_name.replace(" ", "_"))
        os.makedirs(artist_folder, exist_ok=True)
        
        # Create filename (remove special characters)
        filename = f"{song.title.replace('/', '_').replace('?', '')}.txt"
        filepath = os.path.join(artist_folder, filename)
        
        # Save lyrics
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(song.lyrics)
        
        return filepath

# Test function
def test_collector():
    """Test the lyrics collector with one artist"""
    collector = LyricsCollector()
    
    # Test with one artist first
    songs = collector.get_artist_songs("Joanna Newsom", max_songs=3)
    
    if songs:
        print("\nFirst 3 songs found:")
        for i, song in enumerate(songs[:3], 1):
            print(f"{i}. {song.title}")
            # Save the song
            saved_path = collector.save_song(song, "Joanna Newsom")
            print(f"   Saved to: {saved_path}")
    
    return len(songs) > 0

if __name__ == "__main__":
    print("Testing Lyrics Collector...")
    success = test_collector()
    if success:
        print("\nTest successful! Check the 'data/raw/' folder.")
    else:
        print("\nTest failed. Check your API token and internet connection.")