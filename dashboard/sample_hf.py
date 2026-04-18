# Create a small sample for Hugging Face
import pandas as pd

# Load and sample
df_sample = pd.read_csv("../uber_trip_data/uber-raw-data-apr14.csv")
df_sample = df_sample.sample(10000, random_state=42)

# Save
df_sample.to_csv("sample_april.csv", index=False)