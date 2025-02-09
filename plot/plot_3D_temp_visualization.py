import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_3d_temp_plot(df, output_path):
    x_unique = np.sort(df['longitude'].unique())
    y_unique = np.sort(df['latitude'].unique())
    X, Y = np.meshgrid(x_unique, y_unique)
    
    # Calcola la media per anno
    df['year'] = df['start_date'].astype(str).str[:4].astype(int)
    Z = df.pivot_table(index='latitude', 
                      columns='longitude', 
                      values='precipitation',
                      aggfunc='mean').values
    
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z,
                                    colorscale='Viridis',
                                    colorbar=dict(title='Precipitation (mm)'))])
    
    fig.update_layout(
        title='3D Precipitation Distribution (2018-2023 Average)',
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Precipitation (mm)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        width=1000,
        height=800
    )
    
    fig.write_html(f"{output_path}.html")
    fig.write_image(f"{output_path}.png", scale=2)  # scale=2 per migliore risoluzione