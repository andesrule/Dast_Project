import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
from scipy import stats
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output_plots"
ANALYSIS_DIR = BASE_DIR / "output_analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)



def plot_map_grid(df, output_dir):
    from plot_map_grid import create_multi_day_plot
    output_file = output_dir / "multi_day_coverage.png"
    create_multi_day_plot(df, str(output_file))
    print(f"Salvato: {output_file}")

def plot_3d_visualization(df, output_dir):
    from plot_3D_temp_visualization import create_3d_temp_plot
    output_file = output_dir / "precipitation_3d"
    create_3d_temp_plot(df, str(output_file))
    print(f"Salvato: {output_file}.html e {output_file}.png")


def analyze_statistics(df, output_dir):
    print("\nEsecuzione analisi statistiche...")
    

    annual_stats = df.groupby('year').agg({
        'precipitation': ['mean', 'std', 'min', 'max', 'count']
    }).round(3)
    

    spatial_stats = df.groupby(['latitude', 'longitude'])['precipitation'].agg(['mean', 'var']).round(3)
    

    annual_stats.to_csv(output_dir / 'annual_statistics.csv')
    spatial_stats.to_csv(output_dir / 'spatial_statistics.csv')
    print(f"Statistiche salvate in {output_dir}")
    
    return annual_stats, spatial_stats

def analyze_temporal_patterns(df, output_dir):
    print("\nAnalisi pattern temporali...")
    

    yearly_means = df.groupby('year')['precipitation'].mean()
    

    years = np.array(yearly_means.index)
    values = yearly_means.values
    trend_test = stats.kendalltau(years, values)

    pd.DataFrame(yearly_means).to_csv(output_dir / 'temporal_analysis.csv')
    
    with open(output_dir / 'trend_test_results.txt', 'w') as f:
        f.write(f"Trend Test Statistic: {trend_test.statistic:.4f}\n")
        f.write(f"P-value: {trend_test.pvalue:.4f}")
    
    print(f"Analisi temporale salvata in {output_dir}")


def plot_annual_statistics(df, output_dir):
    print("\nGenerazione plot statistiche annuali...")
    yearly_stats = df.groupby('year')['precipitation'].agg(['mean', 'std']).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    

    ax1.plot(yearly_stats['year'], yearly_stats['mean'], 
            marker='o', linewidth=2)
    ax1.set_title('Annual precipitation mean')
    ax1.set_ylabel('Precipitation (mm)')
    ax1.grid(True)

    ax2.plot(yearly_stats['year'], yearly_stats['std'], 
             marker='s', color='orange', linewidth=2)
    ax2.set_title('Annual Standard Deviation')
    ax2.set_xlabel('Anno')
    ax2.set_ylabel('Standard Deviation (mm)')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'annual_statistics_plot.png')
    plt.close()
    print(f"Salvato: {output_dir / 'annual_statistics_plot.png'}")


def plot_spatial_patterns(df, output_dir):
    print("\nGenerazione mappa varianza spaziale...")
    plt.figure(figsize=(12, 8))
    

    spatial_var = df.pivot_table(
        index='latitude',
        columns='longitude',
        values='precipitation',
        aggfunc='var'
    )
    
    sns.heatmap(spatial_var, cmap='YlOrRd')
    plt.title('Varianza Spaziale delle Precipitazioni')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    
    plt.close()

def plot_temporal_analysis(df, output_dir):
    print("\nGenerazione analisi temporale...")
    yearly_stats = df.groupby('year')['precipitation'].agg(['mean', 'std']).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    ax1.plot(yearly_stats['year'], yearly_stats['mean'], 
             marker='o', linewidth=2, label='Mean Precipitation')
    z1 = np.polyfit(yearly_stats['year'], yearly_stats['mean'], 1)
    p1 = np.poly1d(z1)
    ax1.plot(yearly_stats['year'], p1(yearly_stats['year']), '--', color='red', label='Trend')
    ax1.set_title('Temporal Precipitation Trend')
    ax1.set_ylabel('Mean Precipitation (mm)')
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(yearly_stats['year'], yearly_stats['std'], 
             marker='s', color='orange', linewidth=2, label='Standard Deviation')
    z2 = np.polyfit(yearly_stats['year'], yearly_stats['std'], 1)
    p2 = np.poly1d(z2)
    ax2.plot(yearly_stats['year'], p2(yearly_stats['year']), '--', color='red', label='Trend')
    ax2.set_title('Annual Standard Deviation Trend')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Standard Deviation (mm)')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'temporal_trend.png')
    plt.close()
    print(f"Salvato: {output_dir / 'temporal_trend.png'}")

def main():
    print(f"Directory di output visualizzazioni: {OUTPUT_DIR}")
    print(f"Directory di output analisi: {ANALYSIS_DIR}")
    print("Inizializzazione della generazione dei plot e delle analisi...")
    
    print("\nCaricamento dei dati...")
    df = pd.read_csv('precipitation_timeseries.csv')
    df['year'] = df['start_date'].astype(str).str[:4].astype(int)
    
    print("\nGenerazione visualizzazioni di base...")
    plot_temporal_analysis(df, OUTPUT_DIR)
    
    print("\nGenerazione completata! Verifica i file nelle directory:")
    print(f"- Visualizzazioni: {OUTPUT_DIR}")
    print(f"- Analisi: {ANALYSIS_DIR}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Errore durante l'esecuzione: {str(e)}")
