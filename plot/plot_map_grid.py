import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import numpy as np

def create_multi_day_plot(df, output_path, n_days=6):  
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), 
                            subplot_kw={'projection': ccrs.PlateCarree()})
    axes = axes.flatten()
    
    
    df['year'] = df['start_date'].astype(str).str[:4].astype(int)
    grouped = df.groupby('year')
    
    for idx, (year, group) in enumerate(grouped):
        if idx >= n_days:
            break
            
        ax = axes[idx]
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.set_extent([10, 15, 41, 44], crs=ccrs.PlateCarree())
        
        scatter = ax.scatter(group['longitude'], 
                           group['latitude'],
                           c=group['precipitation'],
                           cmap='YlOrRd',
                           transform=ccrs.PlateCarree())
        
        ax.set_title(f'Year {year}')
    
   
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(scatter, cax=cbar_ax, label='Precipitation (mm)')
    
    plt.suptitle('Yearly Precipitation Distribution', fontsize=16)
    
   
    plt.subplots_adjust(top=0.9, right=0.9, left=0.1, bottom=0.1, wspace=0.3, hspace=0.3)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
