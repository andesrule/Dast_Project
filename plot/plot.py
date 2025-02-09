import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_and_prepare_data(file_path):
    
    df = pd.read_csv(file_path)
    
    
    df['year'] = df['start_date'].astype(str).str[:4].astype(int)
    
    return df

def create_time_series_plot(df, ax):
   
    yearly_avg = df.groupby('year')['precipitation'].mean().reset_index()
    
  
    ax.plot(yearly_avg['year'], yearly_avg['precipitation'], 
            marker='o', linewidth=2, markersize=8)
    ax.set_title('Media Annuale delle Precipitazioni (2018-2023)')
    ax.set_xlabel('Anno')
    ax.set_ylabel('Precipitazione Media (mm)')
    ax.grid(True, linestyle='--', alpha=0.7)
    

    for x, y in zip(yearly_avg['year'], yearly_avg['precipitation']):
        ax.text(x, y + 0.05, f'{y:.2f}', ha='center', va='bottom')

def create_spatial_distribution_plot(df, ax):

    pivot = df.pivot_table(
        values='precipitation',
        index='latitude',
        columns='longitude',
        aggfunc='mean'
    )
    

    sns.heatmap(pivot, 
                cmap='YlOrRd',
                ax=ax,
                cbar_kws={'label': 'Precipitazione (mm)'},
                xticklabels=5,
                yticklabels=5)
    
    ax.set_title('Distribuzione Spaziale delle Precipitazioni')
    ax.set_xlabel('Longitudine')
    ax.set_ylabel('Latitudine')

def main():

    df = load_and_prepare_data('precipitation_timeseries.csv')
    
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    fig.suptitle('Analisi delle Precipitazioni', fontsize=16, y=0.95)
    

    create_time_series_plot(df, ax1)
    create_spatial_distribution_plot(df, ax2)
    

    plt.tight_layout()
    

    plt.savefig('precipitation_analysis.png', dpi=300, bbox_inches='tight')
    

    plt.show()

if __name__ == "__main__":
    main()