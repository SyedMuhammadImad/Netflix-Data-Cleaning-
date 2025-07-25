# 📊 Netflix Data Cleaning Project

This project focuses on cleaning and exploring the **Netflix titles dataset** using Python and pandas. It involves removing missing data, extracting useful features, and visualizing key patterns such as content types, top countries, popular genres, and more.

## 🧰 Tools Used
- Python
- pandas
- matplotlib
- numpy

## 📁 Files Included
- [`netflix_data_cleaning.py`](netflix_data_cleaning.py) – The main data cleaning and visualization script
- `netflix_titles.csv` – Dataset from Kaggle (see link below)

## 📌 Project Tasks
- Loaded and inspected Netflix data
- Dropped rows with missing `director` and `country` data
- Converted `date_added` column to datetime format
- Extracted the `year_added` feature
- Visualized:
  - Number of Movies vs TV Shows
  - Top 10 countries by content count
  - Content added over the years
  - Most common genres
  - Top 3 directors with the most titles

## 📊 Sample Visuals
- Bar charts and line plots using `matplotlib.pyplot`
- Genre and country distributions
- Year-over-year trends

## 📚 Dataset Source
[Kaggle – Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

## ✨ Future Improvements
- Turn this into a Streamlit web app
- Add interactivity with filters by year, country, or genre
- Use seaborn for advanced visualizations

---

Feel free to ⭐ this repo or fork it if you're working on similar projects!

