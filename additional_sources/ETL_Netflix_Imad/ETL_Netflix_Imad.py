# ============================================================
# ETL Pipeline — Netflix Movies & TV Shows Dataset
# Name: Muhammad Imad | ID: F2023376179
# Subject: Data Warehousing & Business Intelligence
# Instructor: Dr. Rimsha Anam
# ============================================================

# ============================================================
# INSTALL REQUIRED LIBRARIES
# ============================================================
# Run this cell first in Google Colab
# !pip install gdown pandas sqlalchemy

# ============================================================
# STAGE 1 — EXTRACT
# ============================================================

import gdown
import pandas as pd

# Download Netflix dataset from Google Drive (public Kaggle mirror)
url = "https://drive.google.com/uc?id=1K_Z5LnFCHLgSdNvKxjxcGxAHiQOcvLSs"
output = "/content/netflix_titles.csv"

print("Downloading Netflix dataset...")
gdown.download(url, output, quiet=False)

# Load into DataFrame
df = pd.read_csv(output, encoding="utf-8")

# Inspect the raw data
print("\n--- Data Extracted Successfully ---")
print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
print(f"\nColumn Names:\n{list(df.columns)}")
print(f"\nFirst 5 Records:")
print(df.head())
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values per Column:\n{df.isnull().sum()}")


# ============================================================
# STAGE 2 — TRANSFORM
# ============================================================

print("\n\n========== STAGE 2: TRANSFORM ==========")

# ── PART A: DATA CLEANING ──────────────────────────────────

# 1. Column Renaming — lowercase + underscores
df.columns = df.columns.str.lower().str.replace(" ", "_")
print("\n1) Columns renamed:")
print(list(df.columns))

# 2. Handle Missing Values
print(f"\n2) Missing Values Before Cleaning:\n{df.isnull().sum()}")

# Fill missing director with 'Unknown'
df['director'].fillna('Unknown', inplace=True)

# Fill missing cast with 'Not Listed'
df['cast'].fillna('Not Listed', inplace=True)

# Fill missing country with 'Unknown'
df['country'].fillna('Unknown', inplace=True)

# Fill missing rating with mode (most common rating)
df['rating'].fillna(df['rating'].mode()[0], inplace=True)

# Fill missing duration with 'Unknown'
df['duration'].fillna('Unknown', inplace=True)

# Drop rows where date_added is missing (very few, critical field)
df.dropna(subset=['date_added'], inplace=True)

print(f"\n   Missing Values After Cleaning:\n{df.isnull().sum()}")

# 3. Data Type Fixing
# Strip whitespace from date_added before converting
df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y')

# release_year as integer
df['release_year'] = df['release_year'].astype(int)

print(f"\n3) Data Types After Fixing:\n{df.dtypes}")

# 4. Duplicate Removal
duplicates = df.duplicated().sum()
print(f"\n4) Duplicate Rows Found: {duplicates}")
df.drop_duplicates(inplace=True)
print(f"   Duplicates removed. New shape: {df.shape}")

# 5. Standardize 'type' column values
df['type'] = df['type'].str.strip().str.title()
print(f"\n5) Unique content types: {df['type'].unique()}")


# ── PART B: FEATURE ENGINEERING ───────────────────────────

print("\n--- Part B: Feature Engineering ---")

# 1. added_year — year the title was added to Netflix
df['added_year'] = df['date_added'].dt.year

# 2. added_month — month the title was added
df['added_month'] = df['date_added'].dt.month

# 3. years_since_release — how old the content is when added
df['years_since_release'] = df['added_year'] - df['release_year']

# 4. is_movie — binary flag: 1 if Movie, 0 if TV Show
df['is_movie'] = (df['type'] == 'Movie').astype(int)

print("New Columns Added: added_year, added_month, years_since_release, is_movie")
print(f"\nFinal Shape: {df.shape}")
print(df[['show_id', 'type', 'title', 'release_year', 'added_year',
          'added_month', 'years_since_release', 'is_movie']].head())


# ============================================================
# STAGE 3 — LOAD
# ============================================================

print("\n\n========== STAGE 3: LOAD ==========")

import sqlite3

# Create SQLite database
conn = sqlite3.connect('/content/netflix_warehouse.db')

# Load cleaned DataFrame into SQLite as table 'fact_netflix'
df.to_sql('fact_netflix', conn, if_exists='replace', index=False)

print("Data loaded into: netflix_warehouse.db")
print(f"Table: fact_netflix | Total Records: {len(df)}")

# Verify load
verifyDf = pd.read_sql("SELECT show_id, type, title, country, release_year, added_year FROM fact_netflix LIMIT 5", conn)
print("\nVerification:")
print(verifyDf)


# ============================================================
# SQL ANALYSIS ON LOADED DATA
# ============================================================

print("\n\n========== SQL ANALYSIS ==========")

# Query 1 — Count of Movies vs TV Shows
query1 = pd.read_sql("""
    SELECT type,
           COUNT(*) AS total_titles
    FROM fact_netflix
    GROUP BY type
    ORDER BY total_titles DESC
""", conn)
print("\nQuery 1: Movies vs TV Shows")
print(query1)

# Query 2 — Top 5 Countries by Number of Titles
query2 = pd.read_sql("""
    SELECT country,
           COUNT(*) AS total_titles
    FROM fact_netflix
    WHERE country != 'Unknown'
    GROUP BY country
    ORDER BY total_titles DESC
    LIMIT 5
""", conn)
print("\nQuery 2: Top 5 Countries by Number of Titles")
print(query2)

# Query 3 — Average Years Since Release by Content Type
query3 = pd.read_sql("""
    SELECT type,
           ROUND(AVG(years_since_release), 1) AS avg_years_since_release
    FROM fact_netflix
    GROUP BY type
    ORDER BY avg_years_since_release DESC
""", conn)
print("\nQuery 3: Average Age of Content When Added to Netflix")
print(query3)

conn.close()
print("\n--- ETL Pipeline Complete ---")
