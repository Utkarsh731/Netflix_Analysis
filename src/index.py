from flask import render_template
import pandas as pd

def index_handler(df):
    movie_count = df[df["type"] == "MOVIE"].shape[0]
    show_count = df[df["type"] == "SHOW"].shape[0]
    movie_show_response = [{"type":"MOVIE","total":movie_count, "color":"#E50914"},{"type":"SHOW","total":show_count,"color":"#430000"}]
    print(movie_show_response)
    # Filter the "type" column to only include "MOVIE" and "SHOW"
    df_filtered = df[df['type'].isin(['MOVIE', 'SHOW'])]

    # Group by "release_year" and "type" and count the occurrences
    year_type_count = df_filtered.groupby(['release_year', 'type']).size().reset_index()

    # Pivot the table to have "type" as columns and "total" as values
    year_type_count_pivot = year_type_count.pivot(index='release_year', columns='type', values=0).reset_index()

    # Rename the columns for clarity
    year_type_count_pivot.columns = ['year', 'MOVIE', 'SHOW']

    # Convert the result to a dictionary
    year_type_count_dict = year_type_count_pivot.to_dict(orient='records')

    # Replace NaN values with 0
    for record in year_type_count_dict:
        record['MOVIE'] = record['MOVIE'] if pd.notna(record['MOVIE']) else 0
        record['SHOW'] = record['SHOW'] if pd.notna(record['SHOW']) else 0
        record['year'] = str(record['year'])

    return render_template('index.html', movie_show_response=movie_show_response, yearwise_barchart_response=year_type_count_dict[-1:-20:-1])
