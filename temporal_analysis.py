import pandas as pd
import numpy as np
from scipy import stats

def analyze_temporal_patterns(df):
    print("Analisi pattern temporali...")
    df['year'] = df['start_date'].astype(str).str[:4].astype(int)
    
    yearly_means = df.groupby('year')['precipitation'].mean()
    
    results = {
        'yearly_means': yearly_means
    }
    
    return results

def main():
    df = pd.read_csv('precipitation_timeseries.csv')
    results = analyze_temporal_patterns(df)
    
    pd.DataFrame(results['yearly_means']).to_csv('output_analysis/temporal_analysis.csv')
    
    print("Analisi temporale completata")

if __name__ == "__main__":
    main()