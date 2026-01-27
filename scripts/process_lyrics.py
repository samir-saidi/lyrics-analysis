import os
import sys
import pandas as pd
import re

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Define paths
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
PROCESSED_PATH = os.path.join(DATA_PATH, "processed")
RAW_PATH = os.path.join(DATA_PATH, "raw")

class LyricsProcessor:
    def clean_lyrics(self, lyrics):
        if not isinstance(lyrics, str):
            return ""
               
        return lyrics.strip()
    
    def calculate_basic_counts(self, lyrics):
        clean = self.clean_lyrics(lyrics)
        words = clean.split()
        
        return {
            'cleaned_lyrics': clean,
            'num_words': len(words),
            'num_chars': len(clean)
        }
    
    def process_dataframe(self, df):     
        results = []
        for idx, row in df.iterrows():
            metadata = {
                'artist': row.get('artist', ''),
                'title': row.get('title', ''),
                'album': row.get('album', ''),
            }
            
            counts = self.calculate_basic_counts(row.get('lyrics', ''))
            results.append({**metadata, **counts})
            
            if (idx + 1) % 20 == 0:
                print(f"  Processed {idx + 1}/{len(df)}")
        
        return pd.DataFrame(results)
    
    def run(self):
        """Run minimal processing"""
        # Find raw data
        raw_file = os.path.join(PROCESSED_PATH, "all_songs_raw.csv")
        
        if not os.path.exists(raw_file):
            csv_files = [f for f in os.listdir(PROCESSED_PATH) if f.endswith('.csv')]
            if csv_files:
                raw_file = os.path.join(PROCESSED_PATH, csv_files[0])
            else:
                print("No data found. Run collection script first.")
                return None
        
        print(f"Loading: {raw_file}")
        df = pd.read_csv(raw_file)
        
        # Process
        processed_df = self.process_dataframe(df)
        
        # Save output
        output_file = os.path.join(PROCESSED_PATH, "processed.csv")
        processed_df.to_csv(output_file, index=False)
        print(f"\nSaved processed data to: {output_file}")
        
        return processed_df
    
def main():
    processor = LyricsProcessor()
    df = processor.run()
    
    if df is not None:
        print(f"\nProcessing complete. Total songs: {len(df)}")
        print(f"Artists: {df['artist'].nunique()}")
    
    return df

if __name__ == "__main__":
    main()