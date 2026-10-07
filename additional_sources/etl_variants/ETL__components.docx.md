# Text-only document extract

Source document: ETL__Assignment.docx

Images and layout omitted. Claims below are source text, not independently verified results.

ETL Pipeline — Netflix Dataset

Name: Muhammad Imad

ID: Syed Muhammad Imad

Subject: Data Warehousing & Business Intelligence


Date: 16 April 2026



Introduction

This project demonstrates the implementation of an ETL (Extract, Transform, Load) pipeline using the Netflix Movies and TV Shows dataset. The dataset contains information about titles available on Netflix, including type, release year, country, and date added. The objective is to extract raw data, transform it into a clean and structured format, and load it into a database for analysis.

Stage 1 — Extract

The dataset was extracted from an online source and loaded into a Pandas DataFrame using pd.read_csv(). The structure of the dataset was inspected using head(), shape, and data types to understand its composition.

📌 Insert Screenshot 1 here: Dataset preview (df.head())

Stage 2 — Transform

Part A: Data Cleaning

- Column names were standardized to lowercase with underscores.- Missing values in columns such as director, cast, and country were handled.- date_added column was converted to datetime format.- Duplicate records were removed.- Data types were corrected for consistency.

📌 Insert Screenshot 2 here: Missing values before/after cleaning

Part B: Feature Engineering

- added_year: Extracted from date_added.- added_month: Extracted from date_added.- years_since_release: Difference between added year and release year.- is_movie: Binary indicator for Movie or TV Show.

📌 Insert Screenshot 3 here: New columns preview

Stage 3 — Load

The cleaned dataset was loaded into a SQLite database named netflix.db using the to_sql() function. The table was named fact_netflix and verified by running SQL queries.

📌 Insert Screenshot 4 here: Database load confirmation

SQL Analysis

1. Movies vs TV Shows — shows distribution of content types.

📌 Insert Screenshot 5 here: Query 1 output

2. Top 5 Countries — identifies countries with most content.

📌 Insert Screenshot 6 here: Query 2 output

3. Average Content Age — shows how old content is when added.

📌 Insert Screenshot 7 here: Query 3 output
