

import pandas as pd
import os

def main():
  
    # Load JSON file
   
    
    # Find JSON file inside data folder
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    
    if not files:
        print("No JSON file found in data folder")
        return
    
    filepath = os.path.join("data", files[0])
    
    df = pd.read_json(filepath)
    
    print(f"Loaded {len(df)} stories from {filepath}")
    

    # CLEANING

    
    # 1. Remove duplicates based on post_id
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")
    
    # 2. Remove missing values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")
    
    # 3. Fix data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)
    
    # 4. Remove low quality (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    # 5. Strip whitespace in title
    df["title"] = df["title"].str.strip()
    
  
    # SAVE CSV
  
    
    output_file = "data/trends_clean.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\nSaved {len(df)} rows to {output_file}")
    
  
    # SUMMARY
    
    
    print("\nStories per category:")
    print(df["category"].value_counts())


# Entry point

if __name__ == "__main__":
    main()