import pandas as pd
import re

# Loading dataset
file_path = "AirlineReviews.csv" # Located inside 'data' folder
df = pd.read_csv(file_path)

# Checking 'Review' column and drop NaN values
if "Review" not in df.columns or "Recommended" not in df.columns:
    raise ValueError("Required columns ('Review', 'Recommended') not found in dataset.")

df = df.dropna(subset=["Review", "Recommended"])  # Removing rows with missing values

# Converting 'Recommended' to binary labels (1 for yes, 0 for no)
df['Recommended'] = df['Recommended'].map({'yes': 1, 'no': 0})

def clean_text(text):
    if isinstance(text, str):  # Checking text is string before processing
        text = text.lower()  # Converting to lowercase
        text = re.sub(r'\W+', ' ', text)  # Removing special characters
        return text.strip()
    return ""

df['Review'] = df['Review'].apply(clean_text)

# Saving......
cleaned_file_path = "AirlineReviews_Cleaned.csv"
df.to_csv(cleaned_file_path, index=False)
print(f"Cleaned dataset for sentiment analysis saved: {cleaned_file_path}")
