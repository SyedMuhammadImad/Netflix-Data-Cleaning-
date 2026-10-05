# Text-only document extract

Source document: ETL__Assignment f2023376179.docx

Images and layout omitted. Claims below are source text, not independently verified results.

ETL Pipeline:

Name: Muhammad Imad

ID: F2023376179

Subject: Data Warehousing & Business Intelligence

Instructor: Dr. Rimsha Anam

Date: 16 April 2026

Code link: https://colab.research.google.com/drive/15SUQIvAC8hminfXqopJgZErggxS5qvv7?usp=sharing



Introduction

This assignment demonstrates the implementation of an ETL (Extract, Transform, Load) pipeline using the Netflix Movies and TV Shows dataset. The dataset contains information about titles available on Netflix, including type, release year, country, and date added. The objective is to extract raw data, transform it into a clean and structured format, and load it into a database for analysis.

Stage 1 — Extract

The dataset was extracted from an online source and loaded into a Pandas DataFrame using pd.read_csv(). The structure of the dataset was inspected using head(), shape, and data types to understand its composition.



Stage 2 — Transform

Part A: Data Cleaning

- Column names were standardized to lowercase with underscores.- Missing values in columns such as director, cast, and country were handled.- date_added column was converted to datetime format.- Duplicate records were removed.- Data types were corrected for consistency.



Part B: Feature Engineering

- added_year: Extracted from date_added.- added_month: Extracted from date_added.- years_since_release: Difference between added year and release year.- is_movie: Binary indicator for Movie or TV Show.



Stage 3 — Load

The cleaned dataset was loaded into a SQLite database named netflix.db using the to_sql() function. The table was named fact_netflix and verified by running SQL queries.



SQL Analysis

1. Movies vs TV Shows — shows distribution of content types.



2. Top 5 Countries — identifies countries with most content.



3. Average Content Age — shows how old content is when added.

