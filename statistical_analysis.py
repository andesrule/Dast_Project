import pandas as pd
import numpy as np
from scipy import stats

def analyze_precipitation_stats(df):
    print("Esecuzione analisi statistiche...")
    df['year'] = df['start_date'].astype(str).str[:4].astype(int)
    

    annual_stats = df.groupby('year').agg({
        'precipitation': ['mean', 'std', 'min', 'max', 'count']
    }).round(3)
    

    spatial_stats = df.groupby(['latitude', 'longitude'])['precipitation'].agg(['mean', 'var']).round(3)
    
    return annual_stats, spatial_stats

def main():

    df = pd.read_csv('precipitation_timeseries.csv')
    

    annual_stats, spatial_stats = analyze_precipitation_stats(df)
    

    annual_stats.to_csv('output_analysis/annual_statistics.csv')
    spatial_stats.to_csv('output_analysis/spatial_statistics.csv')
    
    print("Statistiche salvate in output_analysis/")

if __name__ == "__main__":
    main()