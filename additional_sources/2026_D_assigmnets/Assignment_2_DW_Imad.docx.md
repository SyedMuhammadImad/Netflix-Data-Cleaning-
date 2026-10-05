# Text-only document extract

Source document: Assignment_2_DW_Imad.docx

Images and layout omitted. Claims below are source text, not independently verified results.









University of Management & Technology

Department of Artificial Intelligence

CS439 — Data Warehouse and BI  |  Assignment #02  |  Spring 2026





Name

Student ID

Instructor

Due Date

Marks

Muhammad Imad

F2023376179

Dr. Rimsha Anam

16 April, 2026

10





ETL Pipeline — Netflix Movies & TV Shows Dataset





Introduction

In this assignment, an ETL (Extract, Transform, Load) pipeline has been built using a real-world dataset. The dataset used is the Netflix Movies and TV Shows dataset, downloaded from Kaggle. It contains over 8,800 records and 12 columns, covering titles available on Netflix across different countries from 2008 to 2021. The dataset includes content type, title, director, cast, country, date added, release year, rating, duration, and listed genres.

The goal is to extract raw data from its source, clean and transform it into a structured, analysis-ready format, and load it into a SQLite database. The entire pipeline was built in Python using Google Colab.



Dataset Source: https://www.kaggle.com/datasets/shivamb/netflix-shows

Notebook Link: [Paste your Google Colab link here after running]







Stage 1 — Extract

The first stage of the ETL pipeline is Extraction. The Netflix dataset was downloaded directly into the Google Colab environment using the gdown library from a publicly accessible Google Drive link. This approach means anyone with the notebook link can run it without manually uploading the file.

Once downloaded, the dataset was loaded into a pandas DataFrame using pd.read_csv() with UTF-8 encoding. After loading, the raw structure was inspected — total rows and columns, column names, data types, and missing value counts were all printed to understand the state of the raw data before any cleaning.



Key Extraction Steps:

Downloaded dataset using gdown library from Google Drive

Loaded into pandas DataFrame using pd.read_csv()

Inspected shape: rows, columns, data types, missing values

Confirmed raw data had 8,807 rows and 12 columns



Extraction Code:

import gdown, pandas as pd

url = 'https://drive.google.com/uc?id=...'

gdown.download(url, '/content/netflix_titles.csv', quiet=False)

df = pd.read_csv('/content/netflix_titles.csv', encoding='utf-8')

print(f'Rows: {df.shape[0]} | Columns: {df.shape[1]}')

print(df.dtypes)

print(df.isnull().sum())



[ Screenshot: Stage 1 — Dataset loaded, shape printed, columns and missing values shown ]







Stage 2 — Transform

The second stage is Transformation — the most important stage. Raw data from Kaggle rarely arrives in a clean, analysis-ready state. This stage involved two parts: Data Cleaning and Feature Engineering.



Part A: Data Cleaning

i.  Column Renaming: All column names were converted to lowercase and spaces were replaced with underscores. This ensures consistency and makes the columns easier to reference in Python and SQL queries.



df.columns = df.columns.str.lower().str.replace(' ', '_')



ii.  Missing Values Handling: The dataset had missing values across several columns. Each was handled based on its business context:

director — filled with 'Unknown' since many titles have no director listed

cast — filled with 'Not Listed' for titles with no cast information

country — filled with 'Unknown' for titles with no country of origin

rating — filled with the most frequent rating (mode) to preserve data integrity

duration — filled with 'Unknown' for entries with missing duration

date_added — rows with missing date_added were dropped as this is a critical field for time-based analysis



df['director'].fillna('Unknown', inplace=True)

df['cast'].fillna('Not Listed', inplace=True)

df['country'].fillna('Unknown', inplace=True)

df['rating'].fillna(df['rating'].mode()[0], inplace=True)

df.dropna(subset=['date_added'], inplace=True)



iii.  Data Type Fixing: Several columns had incorrect data types and were corrected:

date_added was converted from string to proper datetime format using pd.to_datetime()

release_year was confirmed and cast as integer

type column was standardized with str.title() to ensure consistent casing (Movie / TV Show)



df['date_added'] = df['date_added'].str.strip()

df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y')

df['release_year'] = df['release_year'].astype(int)

df['type'] = df['type'].str.strip().str.title()



iv.  Duplicate Removal: The dataset was checked for duplicate rows. Duplicates were identified and removed to ensure data integrity.



df.drop_duplicates(inplace=True)



[ Screenshot: Part A — Column renaming, missing values before and after, data types fixed, duplicates removed ]



Part B: Feature Engineering

Four new columns were created from existing data to add analytical value that was not directly available in the raw dataset:

added_year: Extracted from date_added — the year the title was added to Netflix. Useful for trend analysis over time.

added_month: Extracted from date_added — the month of addition. Useful for identifying seasonal content patterns.

years_since_release: Calculated as added_year minus release_year. Shows how old a title was when Netflix acquired it.

is_movie: A binary flag — 1 if the content type is Movie, 0 if TV Show. Useful for quick filtering and aggregation.



df['added_year'] = df['date_added'].dt.year

df['added_month'] = df['date_added'].dt.month

df['years_since_release'] = df['added_year'] - df['release_year']

df['is_movie'] = (df['type'] == 'Movie').astype(int)



[ Screenshot: Part B — Feature engineering output, new columns shown with head() ]







Stage 3 — Load

The third and final stage is Loading. The fully cleaned and transformed dataset was loaded into a SQLite database file named netflix_warehouse.db. SQLite was chosen because it requires no external server or installation and integrates seamlessly with Python through the built-in sqlite3 library.

The cleaned DataFrame was saved as a table named fact_netflix using df.to_sql(). Once loaded, the data was read back using a SQL SELECT query to confirm the load was successful and all records were stored correctly.



import sqlite3

conn = sqlite3.connect('/content/netflix_warehouse.db')

df.to_sql('fact_netflix', conn, if_exists='replace', index=False)

verifyDf = pd.read_sql('SELECT show_id, type, title, country, release_year, added_year FROM fact_netflix LIMIT 5', conn)

print(verifyDf)



[ Screenshot: Stage 3 — Data loaded into SQLite, verification query output shown ]







SQL Analysis on Loaded Data

After loading the data into the SQLite database, three SQL queries were executed directly on the fact_netflix table to confirm the data is fully queryable and to derive initial insights.



Query 1 — Count of Movies vs TV Shows

This query grouped all titles by content type and counted how many Movies and TV Shows are available in the dataset. It gives an immediate view of the content distribution on Netflix.

SELECT type, COUNT(*) AS total_titles

FROM fact_netflix

GROUP BY type

ORDER BY total_titles DESC



[ Screenshot: Query 1 — Movies vs TV Shows count output ]



Query 2 — Top 5 Countries by Number of Titles

This query identified which countries produce the most content on Netflix by counting titles per country, excluding entries where the country was unknown. This helps understand the geographic distribution of Netflix content.

SELECT country, COUNT(*) AS total_titles

FROM fact_netflix

WHERE country != 'Unknown'

GROUP BY country

ORDER BY total_titles DESC

LIMIT 5



[ Screenshot: Query 2 — Top 5 countries output ]



Query 3 — Average Age of Content When Added to Netflix

This query calculated the average number of years between a title's original release year and when it was added to Netflix, grouped by content type. This reveals whether Netflix tends to add newer or older content for Movies versus TV Shows.

SELECT type, ROUND(AVG(years_since_release), 1) AS avg_years_since_release

FROM fact_netflix

GROUP BY type

ORDER BY avg_years_since_release DESC



[ Screenshot: Query 3 — Average years since release by content type output ]







Conclusion

This assignment demonstrated a complete ETL pipeline on the Netflix Movies and TV Shows dataset. In the Extract stage, raw data was pulled directly into the Colab environment and its structure was inspected. In the Transform stage, missing values were handled systematically, data types were corrected, duplicates were removed, and four new analytical features were engineered. In the Load stage, the cleaned data was stored in a SQLite database and verified through a SQL query. Three additional SQL queries confirmed the data is fully queryable and ready for business intelligence analysis.



End of Assignment 2