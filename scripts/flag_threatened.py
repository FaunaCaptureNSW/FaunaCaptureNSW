import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

THREATENED_FILE = os.path.join(BASE_DIR, "species_database", "threatened_species_nsw.csv")
DETECTIONS_FILE = os.path.join(BASE_DIR, "camera_traps", "CT_001", "detections.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "analysis", "flagged_threatened_species", "CT_001_threatened.csv")

# Load datasets
threatened = pd.read_csv(THREATENED_FILE)
detections = pd.read_csv(DETECTIONS_FILE)

# Create lookup set
threatened_species = set(threatened["species_name"])

# Check function
def check_threat(species):
    if species in threatened_species:
        return threatened.loc[threatened["species_name"] == species, "status"].values[0]
    return None

# Apply flagging
detections["threatened_status"] = detections["species_name"].apply(check_threat)

# Filter only threatened species
flagged = detections[detections["threatened_status"].notnull()]

# Create output folder if it doesn't exist
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Save output
flagged.to_csv(OUTPUT_FILE, index=False)

print("Done. Threatened species flagged:")
print(flagged)
