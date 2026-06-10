import os
import sys

# Ensure backend is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.generate_datasets import generate_medicines, generate_diagnoses, generate_investigations, MEDICINES, DIAGNOSES, INVESTIGATIONS
import csv
from pathlib import Path
from app.database import init_db

DATA_DIR = Path(__file__).parent / "data"

def write_csv(filename, fieldnames, data):
    filepath = DATA_DIR / filename
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Generated {filename} ({len(data)} rows)")

def main():
    print("Generating datasets...")
    
    meds = generate_medicines()
    if meds:
        write_csv("medicines.csv", meds[0].keys(), meds)
        
    diags = generate_diagnoses()
    if diags:
        write_csv("diagnoses.csv", diags[0].keys(), diags)
        
    invs = generate_investigations()
    if invs:
        write_csv("investigations.csv", invs[0].keys(), invs)
        
    print("Initializing Database...")
    init_db()
    
    print("Backend initialization complete!")

if __name__ == "__main__":
    main()
